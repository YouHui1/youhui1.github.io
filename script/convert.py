import os
import sys
import time
from pathlib import Path
from PIL import Image

def convert_png_to_jpg(input_dir="images", output_dir="res", quality=85,
                       skip_dirs=None, only_new=True, compare_by="mtime"):
    """
    将指定目录中的PNG图片转换为JPG格式

    参数:
        input_dir: 输入目录路径
        output_dir: 输出目录路径
        quality: JPG质量等级 (0-100)，默认85
        skip_dirs: 要跳过的子文件夹列表（相对路径）
        only_new: 是否只转换新增或修改过的文件，默认True
        compare_by: 比较文件的方式，"mtime"（修改时间）或 "size"（文件大小）
    """

    # 确保输入目录存在
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"错误: 输入目录 '{input_dir}' 不存在")
        return False

    if not input_path.is_dir():
        print(f"错误: '{input_dir}' 不是一个目录")
        return False

    # 确保质量参数在有效范围内
    if not 0 <= quality <= 100:
        print(f"警告: 质量参数 {quality} 不在有效范围内 (0-100)，使用默认值85")
        quality = 85

    # 确保比较方式是有效的
    if compare_by not in ["mtime", "size"]:
        print(f"警告: 比较方式 '{compare_by}' 无效，使用默认值'mtime'")
        compare_by = "mtime"

    # 初始化跳过目录列表
    if skip_dirs is None:
        skip_dirs = []

    # 将跳过目录转换为Path对象列表
    skip_paths = [Path(skip_dir) for skip_dir in skip_dirs]

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 统计变量
    converted_count = 0
    skipped_count = 0
    error_count = 0
    skipped_dir_count = 0

    # 遍历输入目录，保持目录结构
    for root, dirs, files in os.walk(input_dir):
        current_dir = Path(root)

        # 获取相对路径（相对于输入目录）
        try:
            relative_path = current_dir.relative_to(input_dir)
        except ValueError:
            relative_path = Path("")

        # 检查当前目录是否在跳过列表中
        skip_current_dir = False
        for skip_path in skip_paths:
            # 检查是否完全匹配或者skip_path是当前路径的父路径
            if skip_path == relative_path or skip_path in relative_path.parents:
                skip_current_dir = True
                break

        if skip_current_dir:
            print(f"⏭  跳过目录: {relative_path}/")
            skipped_dir_count += 1
            # 不遍历这个目录的子目录
            dirs[:] = []
            continue

        # 在输出目录中创建对应的子目录
        output_subdir = output_path / relative_path
        output_subdir.mkdir(parents=True, exist_ok=True)

        for filename in files:
            # 只处理PNG文件
            if filename.lower().endswith('.png'):
                # 构建完整的输入和输出路径
                input_file = Path(root) / filename

                # 生成输出文件名（将.png替换为.jpg）
                output_filename = filename[:-4] + '.jpg'
                output_file = output_subdir / output_filename

                # 检查是否需要跳过转换
                skip_conversion = False
                reason = ""

                # 检查输出文件是否已存在
                if output_file.exists():
                    if only_new:
                        # 根据比较方式决定是否跳过
                        if compare_by == "mtime":
                            # 比较修改时间
                            input_mtime = input_file.stat().st_mtime
                            output_mtime = output_file.stat().st_mtime
                            if input_mtime <= output_mtime:
                                skip_conversion = True
                                reason = "源文件未修改"
                        elif compare_by == "size":
                            # 这里可以添加基于文件内容的比较
                            # 目前简化为比较修改时间
                            input_mtime = input_file.stat().st_mtime
                            output_mtime = output_file.stat().st_mtime
                            if input_mtime <= output_mtime:
                                skip_conversion = True
                                reason = "源文件未修改"
                else:
                    # 输出文件不存在，需要转换
                    skip_conversion = False

                if skip_conversion:
                    print(f"⏭  跳过 {relative_path}/{filename} - {reason}")
                    skipped_count += 1
                    continue

                try:
                    # 打开并转换图片
                    with Image.open(input_file) as img:
                        # 如果图片有透明通道，转换为RGB（使用白色背景）
                        if img.mode in ('RGBA', 'LA', 'P'):
                            # 创建一个白色背景的RGB图像
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))

                            # 如果原图有透明通道，将原图粘贴到白色背景上
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            if img.mode == 'LA':
                                img = img.convert('RGBA')

                            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = rgb_img
                        elif img.mode != 'RGB':
                            # 其他非RGB模式转换为RGB
                            img = img.convert('RGB')

                        # 保存为JPG格式
                        img.save(output_file, 'JPEG', quality=quality, optimize=True)

                    print(f"✓ 转换成功: {relative_path}/{filename} -> {relative_path}/{output_filename}")
                    converted_count += 1

                except Exception as e:
                    print(f"✗ 转换失败: {relative_path}/{filename} - 错误: {str(e)}")
                    error_count += 1
            else:
                # 对于非PNG文件，可以选择复制或跳过
                if filename.lower().endswith(('.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    skipped_count += 1

    # 打印统计信息
    print("\n" + "="*50)
    print("转换完成！")
    print(f"成功转换: {converted_count} 个PNG文件")
    print(f"跳过文件: {skipped_count} 个文件（已存在且未修改）")
    print(f"跳过目录: {skipped_dir_count} 个目录")
    print(f"转换失败: {error_count} 个文件")
    print(f"输出目录: {output_path.resolve()}")
    print(f"比较方式: {compare_by}")
    print("="*50)

    return True

def main():
    """主函数，支持命令行参数"""
    import argparse

    parser = argparse.ArgumentParser(description='将PNG图片转换为JPG格式')
    parser.add_argument('-i', '--input', default='images',
                       help='输入目录 (默认: images)')
    parser.add_argument('-o', '--output', default='res',
                       help='输出目录 (默认: res)')
    parser.add_argument('-q', '--quality', type=int, default=85,
                       help='JPG质量等级 0-100 (默认: 85)')
    parser.add_argument('--skip-dirs', nargs='+', default=[],
                       help='要跳过的子文件夹列表（相对路径）')
    parser.add_argument('--all', action='store_true',
                       help='转换所有文件，包括已存在的（默认只转换新增或修改过的）')
    parser.add_argument('--compare-by', choices=['mtime', 'size'], default='mtime',
                       help='比较文件的方式：mtime(修改时间)或size(文件大小) (默认: mtime)')
    parser.add_argument('--list-formats', action='store_true',
                       help='显示支持的图片格式')

    args = parser.parse_args()

    if args.list_formats:
        print("支持的图片格式:")
        print("PNG, JPG, JPEG, GIF, BMP, TIFF等")
        print("本程序只处理PNG格式文件的转换")
        return

    # 执行转换
    success = convert_png_to_jpg(
        input_dir=args.input,
        output_dir=args.output,
        quality=args.quality,
        skip_dirs=args.skip_dirs,
        only_new=not args.all,  # --all参数为True时，only_new为False
        compare_by=args.compare_by
    )

    if success:
        print("所有操作已完成！")
    else:
        print("转换过程中出现问题。")
        sys.exit(1)

def run_with_fixed_paths():
    """使用固定路径运行转换"""
    skip_dirs = [
        "site_img"
    ]

    success = convert_png_to_jpg(
        input_dir="../image_png",
        output_dir="../images",
        quality=70,
        skip_dirs=skip_dirs,
        only_new=True,
        compare_by="mtime"
    )
    return success

if __name__ == "__main__":
    # 检查PIL库是否安装
    try:
        from PIL import Image
    except ImportError:
        print("错误: 需要安装Pillow库")
        print("请运行: pip install Pillow")
        sys.exit(1)

    # 使用方式1: 使用命令行参数（推荐）
    # main()

    # 使用方式2: 使用固定路径（注释掉上面的main()，取消下面的注释）
    run_with_fixed_paths()

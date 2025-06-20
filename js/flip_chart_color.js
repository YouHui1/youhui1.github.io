function switchPostChart () {
    // 这里为了统一颜色选取的是“明暗模式”下的两种字体颜色，也可以自己定义
    let color = document.documentElement.getAttribute('data-theme') === 'light' ? '#4C4948' : 'rgba(255,255,255,0.7)'
    var color1 = document.documentElement.getAttribute('data-theme') === 'light' ? 'rgba(44, 41, 244, 0.049)' : 'rgba(15,192,192,0.095)'
    var color2 = document.documentElement.getAttribute('data-theme') === 'light' ? 'rgba(255, 85, 0, 0.39)' : 'rgba(192,192,192,0.6)'
    var itemColor = new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
        offset: 0,
        color: color1
      },
      {
        offset: 1,
        color: color2
      }])
      var colorSetDark = [
        "rgba(15, 192, 192, 0.55)",  // 起始颜色（青绿）
        "rgba(33, 192, 192, 0.60)",
        "rgba(51, 192, 192, 0.65)",
        "rgba(69, 192, 192, 0.70)",
        "rgba(87, 192, 192, 0.75)",
        "rgba(105, 192, 192, 0.80)",
        "rgba(123, 192, 192, 0.85)",
        "rgba(141, 192, 192, 0.90)",
        "rgba(160, 192, 192, 0.95)",
        "rgba(192, 192, 192, 0.99)"  // 结束颜色（银白）
      ];
      var colorSetLight = [
        "rgba(44, 41, 244, 0.39)",  // 起始颜色（深蓝）
        "rgba(67, 53, 220, 0.49)",
        "rgba(90, 65, 195, 0.64)",
        "rgba(113, 77, 171, 0.69)",
        "rgba(136, 89, 146, 0.74)",
        "rgba(159, 101, 122, 0.79)",
        "rgba(182, 113, 97, 0.84)",
        "rgba(205, 125, 73, 0.89)",
        "rgba(228, 137, 48, 0.94)",
        "rgba(255, 85, 0, 0.99)"    // 结束颜色（橙红）
      ];

    var colorSet = document.documentElement.getAttribute('data-theme') === 'light' ? colorSetLight : colorSetDark;
    if (document.getElementById('posts-chart') && postsOption) {
      try {
        let postsOptionNew = postsOption
        postsOptionNew.title.textStyle.color = color
        postsOptionNew.xAxis.nameTextStyle.color = color
        postsOptionNew.yAxis.nameTextStyle.color = color
        postsOptionNew.xAxis.axisLabel.color = color
        postsOptionNew.yAxis.axisLabel.color = color
        postsOptionNew.xAxis.axisLine.lineStyle.color = color
        postsOptionNew.yAxis.axisLine.lineStyle.color = color
        postsOptionNew.series[0].markLine.data[0].label.color = color
        postsOptionNew.series[0].itemStyle.color = itemColor
        postsOptionNew.series[0].areaStyle.color = itemColor
        postsChart.setOption(postsOptionNew)
      } catch (error) {
        console.log(error)
      }
    }
    if (document.getElementById('tags-chart') && tagsOption) {
      try {
        let tagsOptionNew = tagsOption
        tagsOptionNew.title.textStyle.color = color
        tagsOptionNew.xAxis.nameTextStyle.color = color
        tagsOptionNew.yAxis.nameTextStyle.color = color
        tagsOptionNew.xAxis.axisLabel.color = color
        tagsOptionNew.yAxis.axisLabel.color = color
        tagsOptionNew.xAxis.axisLine.lineStyle.color = color
        tagsOptionNew.yAxis.axisLine.lineStyle.color = color
        tagsOptionNew.series[0].markLine.data[0].label.color = color
        tagsOptionNew.series[0].itemStyle.color = itemColor
        tagsOptionNew.series[0].emphasis.itemStyle.color = itemColor
        tagsChart.setOption(tagsOptionNew)
      } catch (error) {
        console.log(error)
      }
    }
    if (document.getElementById('categories-chart') && categoriesOption) {
      try {
        let categoriesOptionNew = categoriesOption
        categoriesOptionNew.title.textStyle.color = color
        categoriesOptionNew.legend.textStyle.color = color
        categoriesOptionNew.color = colorSet
        if (!categoryParentFlag) { categoriesOptionNew.series[0].label.color = color }
        categoriesChart.setOption(categoriesOptionNew)
      } catch (error) {
        console.log(error)
      }
    }
  }
  document.getElementById("darkmode").addEventListener("click", function () { setTimeout(switchPostChart, 100) })

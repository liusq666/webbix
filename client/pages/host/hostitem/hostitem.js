Page({

  /**
   * 页面的初始数据
   */
  data: {
    hostgraph:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.showLoading({
      title: 'loding...',
      icon:'loding',
      duration: 100
    })
    this.GET_HOST_ITEM()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  },

  // 根据ID查询主机所有监控项
  GET_HOST_ITEM: function(options) {
    var that = this
    var hostid = that.options.hostid
    wx.request({
      url: "http://127.0.0.1:5000/"+hostid,
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        that.setData({"hostgraph":res.data[hostid]})
        // console.log(that.data.hostgraph)
      }
    })
  }
})
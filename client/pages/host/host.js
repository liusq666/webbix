Page({

  /**
   * 页面的初始数据
   */
  data: {
    allhost:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    this.GET_ALL_HOST()
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

  // 获取所有主机名和对应ID
  GET_ALL_HOST: function() {
    var host = this
    wx.request({
      url: "http://127.0.0.1:5000/ah",
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        host.setData({ 'allhost': res.data})
        // console.log(res.data)
      }
    })
  }
})
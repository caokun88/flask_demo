/**
 * Created by ck on 2017/11/23.
 */
/**
 * 微信分享
 */

// 微信分享
function wechat_share() {
    var data = {
        url : location.href,
        csrf_token: $('meta[name="csrf-token"]').attr('content')
    };
    $.ajax({
        url : '/admin/wechat/api/sign/',
        type : 'post',
        data : data,
        dataType: 'json',
        success : function(res) {
            callback(res.data);
        }
    });
}

function callback (data) {
    var wxurl = location.href;
    var wxtitle = "小饭桌APP下载—创业从这里起步，中国最大的TMT行业创业者服务平台。";
    var wxdes = "优质创业课程培训、专业投融资顾问服务、深度创业内容报道。";
    var wximg = "http://static-image.xfz.cn/share_logo.png";

    wx.config({
        debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
        appId: data.app_id, // 必填，公众号的唯一标识
        timestamp: data.timestamp, // 必填，生成签名的时间戳
        nonceStr: data.noncestr, // 必填，生成签名的随机串
        signature: data.signature,// 必填，签名
        jsApiList: [
            'onMenuShareTimeline',
            'onMenuShareAppMessage'
        ]
    });
    wx.ready(function(){
        wx.onMenuShareTimeline({
            title: wxtitle, // 分享标题
            link: wxurl, // 分享链接
            imgUrl: wximg, // 分享图标
            desc: wxdes,
            success: function () {
                // 用户确认分享后执行的回调函数
            },
            cancel: function () {
                // 用户取消分享后执行的回调函数
            }
        });
        wx.onMenuShareAppMessage({
            title: wxtitle, // 分享标题
            link: wxurl, // 分享链接
            imgUrl: wximg, // 分享图标
            desc: wxdes,
            type: '', // 分享类型,music、video或link，不填默认为link
            dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
            success: function () {
                // 用户确认分享后执行的回调函数
            },
            cancel: function () {
                // 用户取消分享后执行的回调函数
            }
        });
    });
}

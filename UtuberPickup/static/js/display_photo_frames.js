
// 定数
const LOOP_TIMES = 10;
const PHOTO_FRAME_HEIGHT = 500;
const PHOTO_FRAME_WIDTH = 700;
const PHOTO_HEIGHT = 350;
const PHOTO_WIDTH = 600;

// グローバル変数
var playerList=[];
var video_time_list=[];
var player = null;
var swiper = null;

// myload
$(function() {

    // スライダーオブジェクト作成
    setSwiper();

    //額縁取り付け（初期）
    displayPhotoFrames(1);

    //現在日時-1日を取得
    var dt =　new Date();
    dt.setDate(dt.getDate() - 1)
    var targetDate = dt.getFullYear()
        + '-' + formatedZeroPadding(dt.getMonth() + 1)
        + '-' + formatedZeroPadding(dt.getDate());

    // ラベルの対象日を更新
    $("#cldr-target-date").val(targetDate)

    // セレクトボックスに登録するVtuberリストを取得
    getVtuberList();

    // ボタンイベント処理
    setBtnEvent();
});

/* ------------------------------
 ボタンイベント処理
 ------------------------------ */
function setBtnEvent(){

    //filterボタン押下処理
    $('#btn-search').on('click', function() {
      initDisplay();
    });
}

/* ------------------------------
 クロスサイトスクリプト攻撃対策（おまじない）
 ------------------------------ */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* ------------------------------
 クロスサイトスクリプト攻撃対策（おまじない）
 ------------------------------ */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/* ------------------------------
 動画埋め込み処理
 ------------------------------ */
 function embedVideo(id, video_id){

    // 埋め込み動画の基本設定
     player = new YT.Player('photo_' + id , {
         height: PHOTO_HEIGHT,
         width: PHOTO_WIDTH,
         videoId: video_id,
         enablejsapi:1,
         origin:'https://vtuber-livechat-analytics.tk/',
         events: {
             'onStateChange': onPlayerStateChange
         }
     });
     // Playerオブジェクトを保持
    playerList[id] = player;

    // ラベルに時間設定
     $('#lbl-time-' + id).text(video_time_list[id]['start'] + '〜' + video_time_list[id]['end'] )
}

// 埋め込み動画のステータスが変わった時の処理
function onPlayerStateChange(event) {
    // 未再生のとき
    if (event.data == -1) {
        // 呼び出し元のplayerIDを取得
        var id_name = event.target.f.id;
        // player_*からIDを取得
        var id = ('' + id_name).split('_')[1];
        var start_position = formatedTime2Seconds(video_time_list[id]['start']);
        player = playerList[id];
        // 動画の開始位置を設定
        player.seekTo(start_position);
    }
}

/* ------------------------------
 存在するPlayerを削除
 ------------------------------ */
function destroyPlayerList(){
    // Playerが存在する場合は削除
    if(playerList != null && playerList != undefined) {
        for (var id = 0; id < playerList.length; id++) {
                playerList[id].destroy();
        }
        playerList=[];
    }
}

/* ------------------------------
 ゼロパッディング処理
 ------------------------------ */
function formatedZeroPadding(num){
    num += "";
      if (num.length === 1) {
        num = "0" + num;
      }
     return num;
}

/* ------------------------------
 HH:MI:SS形式を秒単位に変換
 ------------------------------ */
function formatedTime2Seconds(time){
    var t = time.split(':');
    var hour = parseInt(t[0]);
    var minute = parseInt(t[1]);
    var second = parseInt(t[2]);
    return hour * 3600 + minute * 60 + second;
}

 /* ------------------------------
 額縁取り付け処理
 ------------------------------ */
function displayPhotoFrames(slide_num){
    for(var num=1; num <= slide_num; num++) {
        var page = '';
        for (var id = 0; id < LOOP_TIMES; id++) {
            var photo_num = id + ((num - 1) * 10);
            page += '<li><div class="photo-frame">'
                + '<img src="../../static/img/gray_background.jpeg" height ="' + PHOTO_FRAME_HEIGHT + 'px" width="' + PHOTO_FRAME_WIDTH + 'px" >'
                + '<div class="rank"><p class="rank-num">No.' + (id + 1) + '</p></div>'
                + '<div class="time"><label class="lbl-time" id="lbl-time-' + photo_num + '"></label></div>'
                + '<div class="photo" id="photo_' + photo_num + '" style="position: absolute; "></div>'
                + '</div></li></ul>';
        }
        // No.10毎に登録
        swiper.appendSlide('<div class="swiper-slide"><ul class= "rank-ul" id="rank-ul"></ul>' + page + '</div>');
        swiper.update();
    }
}

/* ------------------------------
 画面表示処理
 ------------------------------ */
function initDisplay(){

    // 対象日をカレンダーから取得
    var targetDate = $("#cldr-target-date").val();

    // チャンネルIDをセレクトボックスから取得
    var channel_id = $("#selbx-vtuber-name").val();

    // クロスサイトスクリプト攻撃対策用トークン生成
    // event.preventDefault();
    var form = $(this);
    var csrf_token = getCookie("csrftoken");

    // 非同期通信
    $.ajax({
         url: 'getVtuberPhotoFrames/',
         method: 'post',
         data: {func: 'getVtuberPhotoFrames', target_date: targetDate, channel_id: channel_id},
         dataType:"json",
         beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
         },
        success: function(data, status, jqXHR) {

             //動画を埋め込む前にPlayerを削除しておく
             destroyPlayerList();

             //時間リストの初期化
             video_time_list=[];

             //スライドショーの削除
             swiper.removeAllSlides();
             swiper.update();

            //動画埋め込み処理
             if(channel_id == 'NoFilter'){
                 // 氏名フィルターをかけていない場合
                 displayPhotoFrames(1);
                for(var id=0; id < data.length; id++) {
                    video_time_list.push(data[id]['time_list'][0]);
                    embedVideo(id, data[id]['video_id']);
                }
             }else{
                 // 氏名フィルターをかけている場合
                 displayPhotoFrames(data.length == 0 ? 1 : data.length); // 1件もない場合は額縁だけ作る。
                 for(var id=0; id < data.length; id++) {
                     for (var timeId = 0; timeId < Object.keys(data[id]['time_list']).length; timeId++) {
                         video_time_list.push(data[id]['time_list'][timeId]);
                         embedVideo(timeId + (id * 10), data[id]['video_id']);
                     }
                 }
            }
        },
        error: function(xhr, status, error) {
            // エラー内容表示
            alert(status + "\n" +
                    "Status: " + xhr.status + "\n" + error);
        }
     });
}

/* ------------------------------
 Vtuberリスト取得処理
 ------------------------------ */
function getVtuberList(){

    // クロスサイトスクリプト攻撃対策用トークン生成
    // event.preventDefault();
    var form = $(this);
    var csrf_token = getCookie("csrftoken");

    // 非同期通信
    $.ajax({
         url: 'getVtuberPhotoFrames/',
         method: 'post',
         data: {func: 'getVtuberList'},
         dataType:"json",
         beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
         },
        success: function(data, status, jqXHR) {

             // セレクトボックスにVtuberリストを追加
             for(var id=0; id < data.length; id++) {
                 $('#selbx-vtuber-name').append($('<option>').html(data[id]['vtuber_name']).val(data[id]['channel_id']));
             }

            // 画面表示処理
            initDisplay();

        },
        error: function(xhr, status, error) {
            // エラー内容表示
            alert(status + "\n" +
                    "Status: " + xhr.status + "\n" + error);
        }
     });
}

/* ------------------------------
 Swiper初期設定処理
 ------------------------------ */
function setSwiper(){
    swiper = new Swiper('.swiper-container', {
        autoHeight:true,
        effect: "slide",
        loop: false,
        // pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
    });
}
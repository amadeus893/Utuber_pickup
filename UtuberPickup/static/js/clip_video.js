
// 定数
const LOOP_TIMES = 10;

// グローバル変数
var playerList=[];
var video_time_list;
var video_id;
var player = null;


$(function() {

    // Youtube Iframe Api を使うための準備
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // クリアボタン押下
//    $('.clearButton').on('click', clearButton());

    // 実行ボタン押下
    $('#clip_execute').submit( function(event) {

        var target_url = $('#target_url').val();
        // 入力チェック
        if( target_url == '' ){
            removeLoading();
            alert('URLが空欄です');
            return false;
        }

        // 処理前に Loading 画像を表示
        dispLoading("処理中...");

        // Playerの状態を準備中に設定
        player_state = false;

        // クロスサイトスクリプト攻撃対策用トークン生成
        event.preventDefault();
        var form = $(this);
        var csrf_token = getCookie("csrftoken");

        // 非同期通信
        $.ajax({
             url: form.prop('action'),
             method: form.prop('method'),
             data: {target_url: target_url},
             dataType:"json",
             beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
             },
            success: function(data, status, jqXHR) {
                // Lading 画像を消す
                removeLoading();
                // Player毎の初期開始、終了時刻を保持
                video_time_list = data['result'];
                // モデレーターチャット一覧テーブル作成
                createModeratorChatList(data['moderator_chat_list'])
                // ターゲットURLからYoutube動画のIDを取得
                video_id = target_url.split('/')[3];
                // 動画埋め込み処理
                for(var i=0; i < LOOP_TIMES; i++){
                    embedVideo(i);
                }
            },
            error: function(xhr, status, error) {
                // Lading 画像を消す
                removeLoading();
                // エラー内容表示
                alert(status + "\n" +
                        "Status: " + xhr.status + "\n" + error);
            }
         });
    });
});

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
 Loading イメージ表示関数
 引数： msg 画面に表示する文言
 ------------------------------ */
function dispLoading(msg){
  // 引数なし（メッセージなし）を許容
  if( msg == undefined ){
    msg = "";
  }
  // 画面表示メッセージ
  var dispMsg = "<div class='loadingMsg'>" + msg + "</div>";
  // ローディング画像が表示されていない場合のみ出力
  if($("#loading").length == 0){
    $("body").append("<div id='loading'>" + dispMsg + "</div>");
  }
}

/* ------------------------------
 Loading イメージ削除関数
 ------------------------------ */
function removeLoading(){
  $("#loading").remove();
}

/* ------------------------------
 動画埋め込み処理
 ------------------------------ */
 function embedVideo(id){
    // Playerが存在する場合は削除
    if(playerList[id] != undefined){
        playerList[id].destroy();
    }
    // 埋め込み動画の基本設定
    player = new YT.Player('player_' + id , {
        height: '360',
        width: '640',
        videoId: video_id,
        events: {
            'onStateChange': onPlayerStateChange
        }
    });
    // Playerオブジェクトを保持
    playerList[id] = player;
    // 動画の下に開始終了時間を表示
    $('#player_lbl_' + id).text(video_time_list[id]['start'] + ' 〜 ' + video_time_list[id]['end']);
}

// 埋め込み動画のステータスが変わった時の処理
function onPlayerStateChange(event) {
    // 未再生のとき
    if (event.data == -1) {
        // 呼び出し元のplayerIDを取得
        var id_name = event.target.h.id;
        // player_*からIDを取得
        var id = ('' + id_name).split('_')[1];
        var start_position = formatedTime2Seconds(video_time_list[id]['start']);
        player = playerList[id];
        // 動画の開始位置を設定
        player.seekTo(start_position);
    }
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
 モデレーターチャット一覧テーブルに追加
 ------------------------------ */
function createModeratorChatList(moderator_chat_list){
    // レコード削除
    $('#moderator_chat_list tr').remove();
    // ヘッダー追加
    $('#moderator_chat_list').append('<tr><th>時間</th><th>アイコン</th><th>ユーザー名</th><th>コメント</th></tr>');
    // レコード追加
    for(var key in moderator_chat_list){
        $('#moderator_chat_list').append(
                '<tr>'
                + '<td>' + moderator_chat_list[key]['time'] + '</td>'
                + '<td><img src="' + moderator_chat_list[key]['authorPhoto'] + '"></td>'
                + '<td>' + moderator_chat_list[key]['authorName'] + '</td>'
                + '<td>' + moderator_chat_list[key]['text'] + '</td>'
                + '</tr>');
    }
}

/* ------------------------------
 クリアボタン押下処理
 ------------------------------ */
function clearButton(){
	$('#target_url').val("");
 }
# python:3.7.7をベースとします
# latestにしてしまうと、後から構成を変更した際に勝手にバージョンが変わってしまう可能性があるので注意
FROM python:3.7.7

RUN apt-get update && apt-get install -y \
  busybox-static \
  && apt-get clean
RUN apt-get update && apt-get -y install vim
# タイムゾーン設定
ENV TZ=Asia/Tokyo

# 環境変数 PYTHONUNBUFFEREDを設定
ENV PYTHONUNBUFFERED 1
ENV DJANGO_READ_ENV_FILE True
# mkdirコマンドの実行
RUN mkdir /UtuberPickup
# 作業ディレクトリの設定
WORKDIR /UtuberPickup
# requirements.txtを/codeに追加する
ADD requirements.txt /UtuberPickup/
# Pythonのパッケージ管理ツールのpipをアップグレード
RUN pip install --upgrade pip
# pipでrequirements.txtに指定されているパッケージを追加する
RUN pip install -r requirements.txt
# ローカルのディレクトリを/codeに追加する
COPY UtuberPickup /UtuberPickup/

RUN mkdir /var/spool/cron/
RUN mkdir /var/spool/cron/crontabs
COPY UtuberPickup/cron.d/crontab /var/spool/cron/crontabs/root
COPY UtuberPickup/cron.d/regularGetYoutubeComments.sh /var/spool/cron/crontabs/regularGetYoutubeComments.sh

# entrypoint.shを実行
ENTRYPOINT ["./entrypoint.sh"]
FROM nginx:1.12.2-alpine

# デフォルトのconfを消して、別の設定を追加
RUN rm /etc/nginx/default.conf
COPY nginx.conf /etc/nginx/
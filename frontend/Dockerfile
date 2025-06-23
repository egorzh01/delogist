FROM node:22-alpine AS build

WORKDIR /delogist-ux
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /delogist-ux/dist/ /usr/share/nginx/html

VOLUME ["/delogist/static"]

CMD ["nginx", "-g", "daemon off;"]
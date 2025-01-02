FROM node:lts as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . ./
RUN npm run build
RUN npm prune --production

FROM node:lts
LABEL Open State Foundation | Open Spending Frontend <developers@openstate.eu>
WORKDIR /app
COPY --from=build /app/build /app/build
COPY --from=build /app/node_modules /app/node_modules/
COPY package.json .
EXPOSE 3000
ENV NODE_ENV=production
ENTRYPOINT [ "node", "build/index.js"]
# ENTRYPOINT [ "npx", "vite", "preview", "--port", "3000", "--host"]

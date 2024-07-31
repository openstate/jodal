FROM node:lts as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM node:lts
LABEL Open State Foundation | Open Spending Frontend <developers@openstate.eu>
WORKDIR /app
COPY --from=build /app/build /app
RUN echo '{"type": "module"}' > package.json
EXPOSE 3000
ENV NODE_ENV=production
ENTRYPOINT [ "node", "index.js"]
# ENTRYPOINT [ "npx", "vite", "preview", "--port", "3000", "--host"]

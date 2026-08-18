# === STAGE 1: Static Code Compilation Builder Node ===
FROM node:18-alpine AS builder
WORKDIR /app

# Install dependencies mappings securely over clean npm ci locks
COPY package*.json ./
RUN npm ci

# Copy full presentation code structures layout assets
COPY . .

# Inject environment routing parameters variables into compilation tracks
ENV NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
RUN npm run build

# === STAGE 2: Ultra-Lightweight Production Runtime Node ===
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Isolate only compiled client artifacts to minimize cloud container storage metrics
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "run", "start"]

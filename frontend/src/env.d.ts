// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  // 👉 agrega aquí otras variables si tienes más
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

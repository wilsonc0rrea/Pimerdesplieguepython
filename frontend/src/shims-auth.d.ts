declare module '@/stores/auth' {
  export interface User {
    usuario_id: number;
    nombre?: string;
    email?: string;
    [key: string]: any;
  }

  export interface AuthStore {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    login(email: string, password: string): Promise<void>;
    logout(): void;
  }

  export function useAuthStore(): AuthStore;
}

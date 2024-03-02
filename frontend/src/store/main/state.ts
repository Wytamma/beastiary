export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
    notFound?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    disconnected: boolean;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
}

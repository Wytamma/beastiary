export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
}

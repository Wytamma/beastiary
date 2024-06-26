<template>
    <div >
        <v-snackbar  :color="currentNotificationColor" v-model="show">
        <div class="d-flex justify-space-between align-center " >
            <v-progress-circular class="ma-1" indeterminate v-show="showProgress"></v-progress-circular>
            <v-icon large class="ma-1" v-show="notFound">mdi-cancel</v-icon>
            {{ currentNotificationContent }}
            <v-btn text @click.native="close">Close</v-btn>
        </div>
        </v-snackbar>
    </div>
</template>
<script lang="ts">
import { dispatchRemoveNotification } from '@/store/main/actions';
import { readFirstNotification } from '@/store/main/getters';
import { commitRemoveNotification } from '@/store/main/mutations';
import { AppNotification } from '@/store/main/state';
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';

@Component
export default class NotificationsManager extends Vue {
    public show: boolean = false;
    public text: string = '';
    public showProgress: boolean = false;
    public notFound: boolean = false;
    public currentNotification: AppNotification | false = false;

    public async hide() {
        this.show = false;
        await new Promise((resolve, reject) => setTimeout(() => resolve(), 500));
    }

    public async close() {
        await this.hide();
        await this.removeCurrentNotification();
    }

    public async removeCurrentNotification() {
        if (this.currentNotification) {
            commitRemoveNotification(this.$store, this.currentNotification);
        }
    }

    public get firstNotification() {
        return readFirstNotification(this.$store);
    }

    public async setNotification(notification: AppNotification | false) {
        if (this.show) {
            await this.hide();
        }
        if (notification) {
            this.currentNotification = notification;
            this.showProgress = notification.showProgress || false;
            this.notFound = notification.notFound || false;
            this.show = true;
        } else {
            this.currentNotification = false;
        }
    }

    @Watch('firstNotification')
    public async onNotificationChange(
        newNotification: AppNotification | false,
        oldNotification: AppNotification | false,
    ) {
        if (newNotification !== this.currentNotification) {
            await this.setNotification(newNotification);
            if (newNotification) {
                dispatchRemoveNotification(this.$store, { notification: newNotification, timeout: 10000 });
            }
        }
    }

    public get currentNotificationContent() {
        return this.currentNotification && this.currentNotification.content || '';
    }

    public get currentNotificationColor() {
        return this.currentNotification && this.currentNotification.color || 'info';
    }
}
</script>

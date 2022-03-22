<template>
    
</template>

<script lang="ts">
import { dispatchCreateTrace } from '@/store/data/actions';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class FileExplorer extends Vue {
    public path: string = '';

    public submit() {
      dispatchCreateTrace(this.$store, {path: this.path});
    }
}
</script>

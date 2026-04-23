<template>
  <span>
    <v-btn
      color="teal lighten-2"
      dark
      fab
      elevation="2"
      x-small
      @click="openDialog"
    >
      <v-icon dark>
        mdi-plus
      </v-icon>
    </v-btn>
    <input
      ref="fileInput"
      type="file"
      accept=".log,.txt,.tsv,.csv"
      multiple
      style="display: none"
      @change="onFileInputChange"
    />
    <v-dialog
      v-model="dialog"
      max-width="760px"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">Add trace to Beastiary</span>
          <v-spacer></v-spacer>
          <v-btn
            color="red lighten-3"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div class="section-header">
            <div class="section-title">Local files</div>
            <div class="section-subtitle">Load traces directly from this browser session.</div>
          </div>
          <div class="drop-zone mb-4" :class="{ 'drop-zone--active': dragging }"
            @dragover.prevent="dragging = true"
            @dragleave.prevent="dragging = false"
            @drop.prevent="onDrop">
            <v-icon large color="teal lighten-2">mdi-file-upload-outline</v-icon>
            <div class="mt-2">Drop local log files here</div>
          </div>
          <div class="d-flex flex-wrap align-center mb-4">
            <v-btn color="teal lighten-2" dark class="mr-2 mb-2" @click="openFileInput" v-if="!supportsLocalAutoReload">
              Choose local files
            </v-btn>
            <v-btn
              v-else
              outlined
              color="teal lighten-2"
              class="mb-2"
              @click="pickFilesWithAutoReload"
            >
              Choose with auto-reload
            </v-btn>
          </div>
          <div v-if="supportsServerFiles">
            <v-divider class="mb-4"></v-divider>
            <div class="section-header" :class="{ 'section-header--disabled': serverFilesDisabled }">
              <div class="section-title">Server files</div>
              <div class="section-subtitle">Browse and add traces that exist on the Beastiary server.</div>
              <div v-if="serverFilesDisabled" class="section-status">
                Server connection unavailable.
              </div>
            </div>
            <v-form @submit.prevent="submitServerTrace">
              <div class="server-input-row">
                <v-text-field
                  required
                  label="Path to the server log file"
                  v-model="path"
                  class="server-path-field"
                  :disabled="serverFilesDisabled"
                ></v-text-field>
                <v-btn
                  color="primary"
                  text
                  class="server-add-btn"
                  :disabled="serverFilesDisabled"
                  @click="submitServerTrace"
                >
                  Add server trace
                </v-btn>
              </div>
            </v-form>
            <v-list style="max-height: 300px; overflow: auto;" :disabled="serverFilesDisabled">
              <v-list-item v-if="!isRoot">
                <v-list-item-avatar>
                  <v-icon class="grey lighten-1" dark>
                    mdi-folder
                  </v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>..</v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn @click="currentPath = parentDir; listDir()" icon :disabled="serverFilesDisabled">
                    <v-icon color="grey lighten-1">mdi-chevron-right</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
              <v-list-item
                v-for="file in files"
                :key="file.name + file.path"
              >
                <v-list-item-avatar>
                  <v-icon
                    class="grey lighten-1"
                    dark
                    v-if="file.is_dir"
                  >
                    mdi-folder
                  </v-icon>
                  <v-icon
                    class="primary lighten-1"
                    dark
                    v-else
                  >
                    mdi-file
                  </v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title v-text="file.name"></v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn @click="currentPath = file.path; listDir()" icon v-if="file.is_dir" :disabled="serverFilesDisabled">
                    <v-icon color="grey lighten-1">mdi-chevron-right</v-icon>
                  </v-btn>
                  <v-btn @click="path = file.path" icon v-else :disabled="serverFilesDisabled">
                    <v-icon color="primary">mdi-plus</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </span>
</template>

<script lang="ts">
import { api } from '@/api';
import { pickFilesWithHandles } from '@/logParser';
import { LocalTraceState } from '@/interfaces';
import { runtimeCapabilities, supportsFileSystemAccessApi } from '@/runtime';
import { dispatchCreateLocalTrace, dispatchCreateTrace } from '@/store/data/actions';
import { commitAddNotification } from '@/store/main/mutations';
import { readDisconnected, readToken } from '@/store/main/getters';
import { AxiosResponse } from 'axios';
import { Component, Vue } from 'vue-property-decorator';

interface ServerFileEntry {
  name: string;
  path: string;
  is_dir: boolean;
}

@Component
export default class AddTraceButton extends Vue {
  public dialog = false;
  public dragging = false;
  public path = '';
  public currentPath = '';
  public parentDir = '';
  public files: ServerFileEntry[] = [];
  public isRoot = true;
  public supportsServerFiles = runtimeCapabilities.supportsServerFiles;
  public supportsLocalAutoReload = runtimeCapabilities.supportsLocalAutoReload && supportsFileSystemAccessApi();

  get serverFilesDisabled() {
    return this.supportsServerFiles && readDisconnected(this.$store);
  }

  public async openDialog() {
    this.dialog = true;
    this.dragging = false;
    if (this.supportsServerFiles && !this.serverFilesDisabled) {
      await this.resetServerBrowser();
    }
  }

  public openFileInput() {
    (this.$refs.fileInput as HTMLInputElement).click();
  }

  public async onFileInputChange(event: Event) {
    const files = Array.from((event.target as HTMLInputElement).files || []);
    await this.loadLocalFiles(files.map((file) => ({ file })));
    (this.$refs.fileInput as HTMLInputElement).value = '';
  }

  public async onDrop(event: DragEvent) {
    this.dragging = false;
    const files = Array.from(event.dataTransfer?.files || []);
    await this.loadLocalFiles(files.map((file) => ({ file })));
  }

  public async pickFilesWithAutoReload() {
    try {
      const files = await pickFilesWithHandles();
      await this.loadLocalFiles(files);
    } catch (error) {
      const message = (error as Error).message || 'Could not open the browser file picker';
      commitAddNotification(this.$store, { content: message, color: 'warning' });
    }
  }

  public async submitServerTrace() {
    if (this.serverFilesDisabled || !this.path) {
      return;
    }
    await dispatchCreateTrace(this.$store, { path: this.path });
    this.dialog = false;
  }

  public async listDir() {
    if (!this.supportsServerFiles || this.serverFilesDisabled) {
      return;
    }
    let response: AxiosResponse | null = null;
    response = await api.listDirectory(readToken(this.$store), this.currentPath);
    this.files = response.data.files;
    this.currentPath = response.data.path;
    this.parentDir = response.data.parent;
    this.isRoot = response.data.is_root;
  }

  private async loadLocalFiles(files: Array<{ file: File; localFile?: LocalTraceState }>) {
    for (const file of files) {
      await dispatchCreateLocalTrace(this.$store, file);
    }
    if (files.length > 0) {
      this.dialog = false;
    }
  }

  private async resetServerBrowser() {
    this.path = '';
    this.currentPath = '';
    this.parentDir = '';
    this.files = [];
    this.isRoot = true;
    await this.listDir();
  }
}
</script>

<style scoped>
.drop-zone {
  border: 2px dashed #80cbc4;
  border-radius: 8px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: background 0.2s ease;
}

.drop-zone--active {
  background: rgba(128, 203, 196, 0.15);
}

.section-header {
  margin-bottom: 16px;
}

.section-title {
  color: #00897b;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.section-subtitle {
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.95rem;
}

.section-header--disabled {
  opacity: 0.6;
}

.section-status {
  color: #c62828;
  font-size: 0.85rem;
  font-weight: 600;
  margin-top: 6px;
}

.server-input-row {
  align-items: flex-end;
  display: flex;
  gap: 12px;
}

.server-path-field {
  flex: 1 1 auto;
}

.server-add-btn {
  margin-bottom: 18px;
  white-space: nowrap;
}

.theme--dark .section-subtitle {
  color: rgba(255, 255, 255, 0.7);
}

.theme--dark .drop-zone {
  color: rgba(255, 255, 255, 0.7);
}
</style>

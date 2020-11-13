<template>
  <v-card class="mx-auto" max-width="900">
    <v-container fluid class="mx-auto" max-width="800">
      <v-row dense>
        <v-card width="100%">
          <v-img
            :src="post.image"
            class="white--text align-end black"
            contain
            height="300px"
          >
            <v-card-title
              class="teal lighten-1"
              v-text="post.title"
            ></v-card-title>
          </v-img>
          <v-card-actions>
            <v-btn
              text
              v-if="post.category"
              :to="'/list/?category=' + post.category.name"
              >Category > {{ post.category.name }}</v-btn
            >
            <v-icon small>mdi-clock</v-icon>
            {{ public_at_or_none }}
            <v-spacer></v-spacer>
            <v-avatar size="25">
              <img
                v-if="post.author.icon"
                :src="post.author.icon"
                alt="Avatar"
              />
              <v-icon v-else>mdi-emoticon</v-icon>
            </v-avatar>
            <v-btn icon v-if="is_author" :to="update_path">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-card-actions>
          <v-list>
            <v-list-item v-for="tag in post.tags" :key="tag.id">
              <v-btn text :to="'/list/?tag=' + tag.name">{{ tag.name }}</v-btn>
            </v-list-item>
          </v-list>
          <v-card-text>
            <no-ssr>
              <mavon-editor
                class="mavonViewer"
                v-model="post.body"
                defaultOpen="preview"
                :toolbarsFlag="false"
                :subfield="false"
                :editable="false"
                :boxShadow="false"
                :language="'ja'"
              />
            </no-ssr>
          </v-card-text>
        </v-card>
      </v-row>
    </v-container>

    <v-container>
      <v-card width="100%">
        <v-card-title class="headline">{{ comment_num }} Comments</v-card-title>

        <v-list>
          <v-list-item v-for="comment in comments" :key="comment.id">
            <v-list-item-icon>
              <v-avatar size="25">
                <img
                  v-if="comment.author.icon"
                  :src="comment.author.icon"
                  alt="Avatar"
                />
                <v-icon v-else>mdi-emoticon</v-icon>
              </v-avatar>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                v-text="
                  `${comment.author.username}:  ${comment.created_at.substr(
                    5,
                    5
                  )}`
                "
              ></v-list-item-title>
              <v-list-item-subtitle
                v-text="comment.body"
              ></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
        </v-list>
        <v-form>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="message"
                  :append-outer-icon="button"
                  :prepend-icon="icon"
                  filled
                  clear-icon="mdi-close-circle"
                  clearable
                  label="Comment"
                  type="text"
                  placeholder="Hey!!"
                  @click:append="toggleMarker"
                  @click:append-outer="sendMessage"
                  @keypress.enter.native.prevent="sendMessage"
                  @click:prepend="changeIcon"
                  @click:clear="clearMessage"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card>
    </v-container>
  </v-card>
</template>
<script>
export default {
  async asyncData({ app, query, error }) {
    const post = await app.$axios.$get(`/post/${query.id}/`).catch((e) => {
      return [];
    });
    const comments = await app.$axios
      .$get(`/comment/${query.id}/`)
      .catch((e) => {
        return [];
      });
    return {
      update_path: `/update/?id=${query.id}`,
      is_author: post.author.id === app.$auth.user.id ? true : false,
      post: post,
      comments: comments,
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
    };
  },
  data: () => ({
    comment_num: "#",
    show: false,
    message: "",
    marker: true,
    iconIndex: 0,
    icons: [
      "mdi-emoticon",
      "mdi-emoticon-cool",
      "mdi-emoticon-dead",
      "mdi-emoticon-excited",
      "mdi-emoticon-happy",
      "mdi-emoticon-neutral",
      "mdi-emoticon-sad",
      "mdi-emoticon-tongue",
    ],
    buttonIndex: 0,
    buttons: ["mdi-send", "mdi-microphone"],
    markdownOption: {
      readmodel: true,
      htmlcode: true,
      help: true,
      toolbarsFlag: true,
      subfield: true,
      defaultOpen: "preview",
      navigation: true,
      shortCut: true,
      editable: true,
      toolbars: {
        subfield: false,
        preview: true,
      },
    },
  }),

  computed: {
    icon() {
      return this.icons[this.iconIndex];
    },
    button() {
      return this.buttons[this.buttonIndex];
    },
    public_at_or_none() {
      if (typeof this.post.public_at === "string") {
        return this.post.public_at.substr(0, 10);
      } else {
        return None;
      }
    },
  },

  methods: {
    toggleMarker() {
      this.marker = !this.marker;
    },
    async sendMessage() {
      if (this.message.trim().length > 0 && this.buttonIndex === 0) {
        this.buttonIndex = 1;
        await this.$axios
          .$post("/comment/", {
            post_id: this.post.id,
            body: this.message,
            author_id: this.$auth.user.id,
          })
          .then((comment) => {
            this.resetIcon();
            this.clearMessage();
            this.clearComment(comment);
          })
          .catch((e) => {});
        this.buttonIndex = 0;
      }
    },
    clearMessage() {
      this.message = "";
    },
    resetIcon() {
      this.iconIndex = 0;
    },
    changeIcon() {
      this.iconIndex === this.icons.length - 1
        ? (this.iconIndex = 0)
        : this.iconIndex++;
    },
    clearComment(comment) {
      this.comments.push(comment);
    },
  },
};
</script>
<style scoped>
.mavonViewer {
  min-width: 0;
  z-index: 2 !important;
}
</style>

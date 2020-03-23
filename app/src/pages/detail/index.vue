<template>
  <v-card class="mx-auto" max-width="900">
    <v-container fluid class="mx-auto" max-width="800">
      <v-row dense>
        <v-card width="100%">
          <v-img
            :src="src"
            class="white--text align-end"
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
            height="300px"
          >
            <v-card-title v-text="post.title"></v-card-title>
          </v-img>
          <v-card-actions>
            <v-btn
              text
              v-if="post.category"
              :to="'/list/?category=' + post.category.name"
            >Category > {{post.category.name}}</v-btn>

            <v-spacer></v-spacer>
            <v-icon>mdi-emoticon</v-icon>
            <v-btn icon v-if="is_author" :to="update_path">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-card-actions>
          <v-list>
            <v-lsit-item v-for="tag in post.tags" :key="tag.id">
              <v-btn text :to="'/list/?tag=' + tag.name">{{tag.name}}</v-btn>
            </v-lsit-item>
          </v-list>
          <v-card-text>{{post.body}}</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-row>
    </v-container>

    <v-container>
      <v-card width="100%">
        <v-card-title class="headline">{{comment_num}} Comments</v-card-title>

        <v-list>
          <v-list-item v-for="comment in comments" :key="comment.id">
            <v-list-item-icon>
              <v-icon>mdi-emoticon</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="comment.body"></v-list-item-title>
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
                  :append-outer-icon="message ? 'mdi-send' : 'mdi-microphone'"
                  :prepend-icon="icon"
                  filled
                  clear-icon="mdi-close-circle"
                  clearable
                  label="Comment"
                  type="text"
                  @click:append="toggleMarker"
                  @click:append-outer="sendMessage"
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
    const post = await app.$axios.$get(`/post/${query.id}/`).catch(e => {
      return [];
    });
    const comments = await app.$axios.$get(`/comment/${query.id}/`).catch(e => {
      return [];
    });
    return {
      update_path: `/update/?id=${query.id}`,
      is_author: post.author.id === app.$auth.user.id ? true : false,
      post: post,
      comments: comments,
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg"
    };
  },
  data: () => ({
    comment_num: "#",
    show: false,
    message: "Hey!",
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
      "mdi-emoticon-tongue"
    ]
  }),

  computed: {
    icon() {
      return this.icons[this.iconIndex];
    }
  },

  methods: {
    toggleMarker() {
      this.marker = !this.marker;
    },
    async sendMessage() {
      await this.$axios
        .$post("/comment/", {
          post_id: this.post.id,
          body: this.message,
          author_id: 1
        })
        .then(comment => {
          this.resetIcon();
          this.clearMessage();
          this.addComment(comment);
        })
        .catch(e => {});
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
    }
  }
};
</script>
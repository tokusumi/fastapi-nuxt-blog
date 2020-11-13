<template>
  <v-app>
    <v-container class="px-0">
      <v-card class="mx-auto" max-width="800px" flat>
        <v-container class="px-0">
          <v-row dense>
            <v-col
              v-for="card in cards"
              :key="card.title"
              cols="12"
              xs="12"
              sm="6"
            >
              <v-card>
                <v-img
                  v-if="card.image"
                  :src="card.image"
                  class="white--text align-end"
                  min-height="300px"
                >
                  <v-card-title
                    class="teal lighten-1 post-title"
                    v-text="card.title"
                  ></v-card-title>
                </v-img>
                <v-img
                  v-else
                  :src="src"
                  class="white--text align-end"
                  height="300px"
                >
                  <v-card-title
                    class="teal lighten-1 post-title"
                    v-text="card.title"
                  ></v-card-title>
                </v-img>
                <v-card-actions>
                  <v-avatar size="35">
                    <img
                      v-if="card.author.icon"
                      :src="card.author.icon"
                      alt="Avatar"
                    />
                    <v-icon v-else>mdi-emoticon</v-icon>
                  </v-avatar>
                  <v-card-text>
                    {{ card.author.username }} |
                    <v-icon small>mdi-clock</v-icon>
                    {{ card.public_at.substr(0, 10) }}
                  </v-card-text>
                  <v-spacer></v-spacer>
                  <v-btn
                    class="teal--text lighten-1"
                    text
                    :to="'/detail/?id=' + card.id"
                    >Show...</v-btn
                  >
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <v-card>
          <div class="text-center">
            <v-pagination
              color="teal lighten-1"
              v-model="page"
              :length="max_page"
              :total-visible="pagination_len"
              @input="getPosts"
              circle
            ></v-pagination>
          </div>
        </v-card>
      </v-card>
    </v-container>
  </v-app>
</template>
<script>
export default {
  async asyncData({ app }) {
    const data = await app.$axios
      .$get("/post/?is_private=false", {
        params: { page: 1, length: 6 },
      })
      .then((data) => {
        return data;
      })
      .catch((err) => {
        console.log(err);
        return {
          data: [],
          max_page: 1,
        };
      });
    return {
      cards: data.data,
      max_page: data.max_page,
      page: 1,
      length: 6,
      pagination_len: 8,
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
    };
  },
  methods: {
    getPosts() {
      this.$axios
        .$get("/post/?is_private=false", {
          params: { page: this.page, length: this.length },
        })
        .then((data) => {
          this.cards = data.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
};
</script>
<style scoped>
.post-title {
  opacity: 0.9;
}
</style>
<template>
  <v-card class="mx-auto" max-width="1000">
    <v-container fluid>
      <v-row dense>
        <v-col v-for="card in cards" :key="card.title" :cols="6">
          <v-card>
            <v-img
              :src="src"
              class="white--text align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              height="300px"
            >
              <v-card-title v-text="card.title"></v-card-title>
            </v-img>

            <v-card-actions>
              <v-avatar size="25">
                <img v-if="card.author.icon" :src="card.author.icon" alt="Avatar" />
                <v-icon v-else>mdi-emoticon</v-icon>
              </v-avatar>
              <v-spacer></v-spacer>

              <v-btn text :to="'/detail/?id=' + card.id">Show...</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div class="text-center">
      <v-pagination
        v-model="page"
        :length="max_page"
        :total-visible="pagination_len"
        @input="getPosts"
        circle
      ></v-pagination>
    </div>
  </v-card>
</template>
<script>
export default {
  async asyncData({ app }) {
    const data = await app.$axios
      .$get("/post/?is_private=false", {
        params: { page: 1, length: 4 }
      })
      .then(data => {
        return data;
      })
      .catch(err => {
        console.log(err);
        return {
          data: [],
          max_page: 1
        };
      });
    return {
      cards: data.data,
      max_page: data.max_page,
      page: 1,
      length: 4,
      pagination_len: 6,
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg"
    };
  },
  methods: {
    getPosts() {
      this.$axios
        .$get("/post/?is_private=false", {
          params: { page: this.page, length: this.length }
        })
        .then(data => {
          this.cards = data.data;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>
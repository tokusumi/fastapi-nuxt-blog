<template>
  <v-card class="mx-auto" max-width="1000">
    <v-container fluid>
      <v-row dense>
        <!-- <v-col v-for="card in cards" :key="card.title" :cols="card.flex"> -->
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
              <v-spacer></v-spacer>

              <v-btn text :to="'/detail/?id=' + card.id">Show...</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div class="text-center">
      <v-pagination v-model="page" :length="length" circle></v-pagination>
    </div>
  </v-card>
</template>
<script>
export default {
  async asyncData({ app }) {
    const data = await app.$axios.$get("http://fastapi:80/post/");
    return {
      cards: data,
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg"
    };
  },
  data: () => ({
    length: 4,
    page: 1
  })
};
</script>
<template>
  <v-form>
    <v-container fluid>
      <v-text-field v-model="title" label="Title" required></v-text-field>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select v-model="select_category" :items="categories" label="Category" dense></v-select>
        </v-col>

        <v-col class="d-flex" cols="12" sm="6">
          <v-select v-model="select_series" :items="serieses" label="Series" dense></v-select>
        </v-col>
        <v-col cols="12" sm="12">
          <v-select v-model="select_tags" :items="tags" label="Select tags" multiple chips></v-select>
        </v-col>
      </v-row>
      <v-textarea v-model="body" name="body" filled label="Body" auto-grow :value="body" required></v-textarea>
      <v-switch v-model="notify_switch" :label="`${notifyMessage()}`"></v-switch>
      <v-switch v-model="publish_switch" :label="`${publishMessage()}`"></v-switch>
    </v-container>
    <v-divider></v-divider>
    <v-btn @click="clear">Clear</v-btn>
    <v-btn class="mr-4" @click="submit">Submit</v-btn>
  </v-form>
</template>
<script>
export default {
  async asyncData({ app, query, error }) {
    let categories = await app.$axios.$get("/category/").catch(e => {
      return [];
    });
    const serieses = await app.$axios.$get("/series/").catch(e => {
      return [];
    });
    const tags = await app.$axios.$get("/tag/").catch(e => {
      return [];
    });

    return {
      categories: categories.map(x => {
        return x.name;
      }),
      serieses: serieses.map(x => {
        return x.name;
      }),
      tags: tags.map(x => {
        return x.name;
      }),
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg"
    };
  },
  data: () => ({
    title: "",
    body: "",
    select_tags: [],
    select_category: "",
    select_series: "",
    notify_switch: true,
    publish_switch: false,
    isLoading: false,
    form: false
  }),
  methods: {
    notifyMessage() {
      if (this.notify_switch === true) {
        return "notify: send email";
      } else {
        return "silent: does not notify";
      }
    },
    publishMessage() {
      if (this.publish_switch === true) {
        return "public: all user will be able to read this.";
      } else {
        return "private: you can only read this.";
      }
    },
    async submit() {
      await this.$axios
        .$post("/post/", {
          title: this.title,
          body: this.body,
          is_public: this.publish_switch,
          notification: this.notify_switch,
          author_id: 1,
          category: this.select_category,
          series: this.select_series,
          tags: this.select_tags
        })
        .then(res => {
          console.log("success");
          this.clear();
        })
        .catch(e => {});
    },
    clear() {
      this.title = "";
      this.body = "";
      this.select_tags = [];
      this.select_category = "";
      this.select_series = "";
    }
  }
};
</script>
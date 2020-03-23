<template>
  <v-form>
    <v-container fluid>
      <v-text-field v-model="post.title" label="Title" required></v-text-field>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select v-model="post.select_category" :items="categories" label="Category" dense></v-select>
        </v-col>

        <v-col class="d-flex" cols="12" sm="6">
          <v-select v-model="post.select_series" :items="serieses" label="Series" dense></v-select>
        </v-col>
        <v-col cols="12" sm="12">
          <v-select v-model="post.select_tags" :items="tags" label="Select tags" multiple chips></v-select>
        </v-col>
      </v-row>
      <v-textarea
        v-model="post.body"
        name="body"
        filled
        label="Body"
        auto-grow
        :value="post.body"
        required
      ></v-textarea>
      <v-switch v-model="post.notify_switch" :label="`${notifyMessage()}`"></v-switch>
      <v-switch v-model="post.publish_switch" :label="`${publishMessage()}`"></v-switch>
    </v-container>
    <v-divider></v-divider>
    <v-btn @click="clear">Clear</v-btn>
    <v-btn class="mr-4" @click="submit">Submit</v-btn>
  </v-form>
</template>
<script>
export default {
  async asyncData({ app, query, error }) {
    const post = await app.$axios
      .$get(`/post/${query.id}/`)
      .then(data => {
        return {
          id: data.id,
          title: data.title,
          body: data.body,
          select_tags: data.tags
            ? data.tags.map(x => {
                return x.name;
              })
            : [],
          select_category: data.category ? data.category.name : "",
          select_series: data.series ? data.series.name : "",
          notify_switch: data.notification,
          publish_switch: data.is_public
        };
      })
      .catch(e => {
        return {
          title: "",
          body: "",
          select_tags: [],
          select_category: "",
          select_series: "",
          notify_switch: true,
          publish_switch: false
        };
      });
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
      post: post,
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
    isLoading: false,
    form: false
  }),
  methods: {
    notifyMessage() {
      if (this.post.notify_switch === true) {
        return "notify: send email";
      } else {
        return "silent: does not notify";
      }
    },
    publishMessage() {
      if (this.post.publish_switch === true) {
        return "public: all user will be able to read this.";
      } else {
        return "private: you can only read this.";
      }
    },
    async submit() {
      await this.$axios
        .$put(`/post/${this.post.id}/`, {
          title: this.post.title,
          body: this.post.body,
          is_public: this.post.publish_switch,
          notification: this.post.notify_switch,
          author_id: this.$auth.user.id,
          category: this.post.select_category,
          series: this.post.select_series,
          tags: this.post.select_tags
        })
        .then(res => {
          console.log("success");
          this.clear();
          this.$router.push(`/detail/?id=${res.id}`);
        })
        .catch(e => {
          console.log(e);
        });
    },
    clear() {
      this.post.title = "";
      this.post.body = "";
      this.post.select_tags = [];
      this.post.select_category = "";
      this.post.select_series = "";
    }
  }
};
</script>
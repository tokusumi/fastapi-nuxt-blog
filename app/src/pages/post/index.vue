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
      <div class="mavonEditor">
        <no-ssr>
          <mavon-editor
            ref="md"
            v-model="body"
            :toolbars="markdownOption"
            :language="'ja'"
            @imgAdd="imgAdd"
          />
        </no-ssr>
      </div>
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
    form: false,
    markdownOption: {
      bold: true,
      italic: true,
      header: true,
      underline: true,
      strikethrough: true,
      mark: true,
      superscript: true,
      subscript: true,
      quote: true,
      ol: true,
      ul: true,
      link: true,
      imagelink: true,
      code: true,
      table: true,
      fullscreen: true,
      readmodel: true,
      htmlcode: true,
      help: true
    }
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
          this.$router.push(`/detail/?id=${res.id}`);
        })
        .catch(e => {
          console.log(e);
        });
    },
    clear() {
      this.title = "";
      this.body = "";
      this.select_tags = [];
      this.select_category = "";
      this.select_series = "";
    },
    imgAdd(pos, $file) {
      let formData = new FormData();
      formData.append("file", $file);
      this.$axios
        .$post("/image/doc/", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(res => {
          this.$refs.md.$img2Url(pos, res.image);
        })
        .catch(errorMsg => alert(errorMsg))
        .finally(() => {
          return false;
        });
    }
  }
};
</script>
<style scoped>
.mavonEditor {
  width: 100%;
  height: "500px";
}
</style>
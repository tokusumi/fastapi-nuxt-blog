<template>
  <v-form>
    <v-container fluid>
      <file-upload
        class="mr-4"
        :endpoint="endpoint"
        v-on:fileUploadEvent="changeMainImg"
        v-on:fileSelectEvent="selectMainImg"
      />
      <v-img class="white--text align-end" contain height="300px" :src="mainImgUrl" alt="MainImg" />

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
      <div class="mavonEditor">
        <no-ssr>
          <mavon-editor
            ref="md"
            v-model="post.body"
            :toolbars="markdownOption"
            :language="'ja'"
            @imgAdd="imgAdd"
          />
        </no-ssr>
      </div>
      <v-switch v-model="post.notify_switch" :label="`${notifyMessage()}`"></v-switch>
      <v-switch v-model="post.publish_switch" :label="`${publishMessage()}`"></v-switch>
    </v-container>
    <v-divider></v-divider>
    <v-btn @click="clear">Clear</v-btn>
    <v-btn class="mr-4" @click="submit">Submit</v-btn>
  </v-form>
</template>
<script>
import FileUpload from "@/components/FileUpload.vue";
export default {
  pageTitle: "PostUpdate",
  components: {
    FileUpload
  },
  async asyncData({ app, query, error }) {
    const post = await app.$axios
      .$get(`/post/${query.id}/`)
      .then(data => {
        return {
          id: data.id,
          title: data.title,
          body: data.body,
          image: data.image,
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
          image: "",
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
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
      mainImgUrl: post.image
    };
  },
  data: () => ({
    endpoint: "/image/",
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
          image: this.post.image,
          is_public: this.post.publish_switch,
          notification: this.post.notify_switch,
          author_id: this.$auth.user.id,
          category: this.post.select_category,
          series: this.post.select_series,
          tags: this.post.select_tags
        })
        .then(res => {
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
      this.post.iamge = "";
      this.mainImgUrl = "";
      this.post.select_tags = [];
      this.post.select_category = "";
      this.post.select_series = "";
    },
    selectMainImg(resCode, target) {
      let reader = new FileReader();
      reader.onload = e => {
        this.mainImgUrl = e.target.result;
      };
      reader.readAsDataURL(target.files[0]);
    },
    changeMainImg(resCode, data) {
      this.mainImgUrl = data.image;
      this.post.image = data.image;
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
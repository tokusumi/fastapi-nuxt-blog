<template>
  <v-form>
    <v-container fluid>
      <file-upload
        class="mr-4"
        :endpoint="endpoint"
        v-on:fileUploadEvent="changeMainImg"
        v-on:fileSelectEvent="selectMainImg"
      />
      <v-img
        class="white--text align-end"
        contain
        height="300px"
        :src="mainImgUrl"
        alt="MainImg"
      />
      <v-col cols="12" sm="12" md="12">
        <select-date :date="post.public_at" v-on:save="saveDate"></select-date>
      </v-col>
      <v-col cols="12" sm="12" md="12">
        <v-text-field
          v-model="post.title"
          label="Title"
          required
        ></v-text-field>
      </v-col>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            v-model="post.select_category"
            :items="categories"
            label="Category"
            dense
          ></v-select>
          <add-dialog
            :endpoint="categoryEndpoint"
            field="category"
            v-on:new="reflesh"
          ></add-dialog>
        </v-col>

        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            v-model="post.select_series"
            :items="serieses"
            label="Series"
            dense
          ></v-select>
          <add-dialog
            :endpoint="seriesEndpoint"
            field="series"
            v-on:new="reflesh"
          ></add-dialog>
        </v-col>
        <v-col class="d-flex" cols="12" sm="12">
          <v-select
            v-model="post.select_tags"
            :items="tags"
            label="Select tags"
            multiple
            chips
          ></v-select>
          <add-dialog
            :endpoint="tagEndpoint"
            field="tag"
            v-on:new="reflesh"
          ></add-dialog>
        </v-col>
      </v-row>
      <no-ssr>
        <mavon-editor
          class="mavonEditor"
          ref="md"
          v-model="post.body"
          :toolbars="markdownOption"
          :language="'ja'"
          @imgAdd="imgAdd"
        />
      </no-ssr>
      <v-switch
        color="teal lighten-1"
        v-model="post.notify_switch"
        :label="`${notifyMessage()}`"
      ></v-switch>
      <v-switch
        color="teal lighten-1"
        v-model="post.publish_switch"
        :label="`${publishMessage()}`"
      ></v-switch>
    </v-container>
    <v-divider></v-divider>
    <v-btn @click="clear">Clear</v-btn>
    <v-btn
      class="mr-4"
      color="teal lighten-1"
      :loading="loading"
      @click="submit"
      >Submit</v-btn
    >
  </v-form>
</template>
<script>
import FileUpload from "~/components/FileUpload.vue";
import AddDialog from "~/components/AddDialog.vue";
import SelectDate from "~/components/SelectDate.vue";
export default {
  pageTitle: "PostUpdate",
  components: {
    FileUpload,
    AddDialog,
    SelectDate,
  },
  async asyncData({ app, query, error }) {
    const post = await app.$axios
      .$get(`/post/${query.id}/`)
      .then((data) => {
        return {
          id: data.id,
          title: data.title,
          body: data.body,
          image: data.image,
          public_at: data.public_at,
          select_tags: data.tags
            ? data.tags.map((x) => {
                return x.name;
              })
            : [],
          select_category: data.category ? data.category.name : "",
          select_series: data.series ? data.series.name : "",
          notify_switch: data.notification,
          publish_switch: data.is_public,
        };
      })
      .catch((e) => {
        return {
          title: "",
          body: "",
          image: "",
          public_at: null,
          select_tags: [],
          select_category: "",
          select_series: "",
          notify_switch: true,
          publish_switch: false,
        };
      });
    const getValue = async function (endpoint, axios) {
      const values = await axios
        .$get(endpoint)
        .then((res) => {
          return res.map((x) => {
            return x.name;
          });
        })
        .catch((e) => {
          return [];
        });
      return values;
    };

    return {
      post: post,
      categoryEndpoint: "/category/",
      seriesEndpoint: "/series/",
      tagEndpoint: "/tag/",
      categories: await getValue("/category/", app.$axios),
      serieses: await getValue("/series/", app.$axios),
      tags: await getValue("/tag/", app.$axios),
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
      mainImgUrl: post.image,
    };
  },
  data: () => ({
    endpoint: "/image/",
    loading: false,
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
      code: false,
      table: true,
      fullscreen: false,
      readmodel: true,
      htmlcode: true,
      help: true,
    },
  }),
  methods: {
    async getValue(endpoint, axios) {
      const out = await axios
        .$get(endpoint)
        .then((res) => {
          return res.map((x) => {
            return x.name;
          });
        })
        .catch((e) => {
          return [];
        });
      return out;
    },
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
          public_at: this.post.public_at,
          author_id: this.$auth.user.id,
          category: this.post.select_category,
          series: this.post.select_series,
          tags: this.post.select_tags,
        })
        .then((res) => {
          this.clear();
          this.$router.push(`/detail/?id=${res.id}`);
        })
        .catch((e) => {
          console.log(e);
        });
    },
    clear() {
      this.post.title = "";
      this.post.body = "";
      this.post.iamge = "";
      this.mainImgUrl = "";
      this.post.public_at = null;
      this.post.select_tags = [];
      this.post.select_category = "";
      this.post.select_series = "";
    },
    async reflesh(endpoint) {
      switch (endpoint) {
        case this.categoryEndpoint:
          this.categories = await this.getValue(endpoint, this.$axios);
          break;
        case this.seriesEndpoint:
          this.serieses = await this.getValue(endpoint, this.$axios);
          break;
        case this.tagEndpoint:
          this.tags = await this.getValue(endpoint, this.$axios);
          break;
      }
    },
    selectMainImg(resCode, target) {
      let reader = new FileReader();
      reader.onload = (e) => {
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
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          this.$refs.md.$img2Url(pos, res.image);
        })
        .catch((errorMsg) => alert(errorMsg))
        .finally(() => {
          return false;
        });
    },
    saveDate(date) {
      this.post.public_at = date;
    },
  },
};
</script>
<style scoped>
.mavonEditor {
  width: 100%;
  height: "500px";
  z-index: 2 !important;
}
</style>
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
        <select-date :date="public_at" v-on:save="saveDate"></select-date>
      </v-col>
      <v-col cols="12" sm="12" md="12">
        <v-text-field v-model="title" label="Title" required></v-text-field>
      </v-col>

      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            v-model="select_category"
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
            v-model="select_series"
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
            v-model="select_tags"
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
          v-model="body"
          :toolbars="markdownOption"
          :language="'ja'"
          @imgAdd="imgAdd"
        />
      </no-ssr>
      <v-switch
        color="teal lighten-1"
        v-model="notify_switch"
        :label="`${notifyMessage()}`"
      ></v-switch>
      <v-switch
        color="teal lighten-1"
        v-model="publish_switch"
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
  pageTitle: "PostCreate",
  components: {
    FileUpload,
    AddDialog,
    SelectDate,
  },
  async asyncData({ app, query, error }) {
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
      categoryEndpoint: "/category/",
      seriesEndpoint: "/series/",
      tagEndpoint: "/tag/",
      categories: await getValue("/category/", app.$axios),
      serieses: await getValue("/series/", app.$axios),
      tags: await getValue("/tag/", app.$axios),
      src: "https://cdn.vuetifyjs.com/images/cards/road.jpg",
      public_at: app.$dayjs().format("YYYY-MM-DDTHH:mm:ss"),
    };
  },
  data: () => ({
    endpoint: "/image/",
    title: "",
    body: "",
    image: "",
    mainImgUrl: "",
    select_tags: [],
    select_category: "",
    select_series: "",
    notify_switch: true,
    publish_switch: false,
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
      this.loading = true;
      await this.$axios
        .$post("/post/", {
          title: this.title,
          body: this.body,
          image: this.image,
          is_public: this.publish_switch,
          notification: this.notify_switch,
          public_at: this.public_at,
          author_id: this.$auth.user.id,
          category: this.select_category,
          series: this.select_series,
          tags: this.select_tags,
        })
        .then((res) => {
          this.clear();
          this.$router.push(`/detail/?id=${res.id}`);
        })
        .catch((e) => {
          console.log(e);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    clear() {
      this.title = "";
      this.body = "";
      this.iamge = "";
      this.mainImgUrl = "";
      this.public_at = this.$dayjs().format("YYYY-MM-DDTHH:mm:ss");
      this.select_tags = [];
      this.select_category = "";
      this.select_series = "";
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
      this.image = data.image;
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
      this.public_at = date;
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
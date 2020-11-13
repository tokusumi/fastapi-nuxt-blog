<template>
  <v-dialog v-model="dialog" max-width="500px">
    <template v-slot:activator="{ on }">
      <v-icon small class="mr-2" v-on="on">mdi-pencil</v-icon>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">New Item</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="12" md="12">
              <select-date
                :date="post.public_at"
                v-on:save="saveDate"
              ></select-date>
            </v-col>
            <v-col cols="12" sm="12" md="12">
              <v-text-field v-model="post.title" label="Title"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <add-dialog
                :endpoint="categoryEndpoint"
                field="category"
                v-on:new="reflesh"
              ></add-dialog>
              <v-select
                v-model="post.category"
                :items="categories"
                label="Categories"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <add-dialog
                :endpoint="seriesEndpoint"
                field="series"
                v-on:new="reflesh"
              ></add-dialog>
              <v-select
                v-model="post.series"
                :items="serieses"
                label="Series"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="8">
              <add-dialog
                :endpoint="tagEndpoint"
                field="tag"
                v-on:new="reflesh"
              ></add-dialog>
              <v-select
                v-model="post.tags"
                :items="tags"
                label="Tags"
                multiple
                chips
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-switch
                v-model="post.is_public"
                :label="`${publishMessage()}`"
              ></v-switch>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="editPost">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import AddDialog from "~/components/AddDialog.vue";
import SelectDate from "~/components/SelectDate.vue";
export default {
  name: "EditItem",
  components: {
    AddDialog,
    SelectDate,
  },
  props: {
    item: { type: Object },
    categories: { type: Array },
    serieses: { type: Array },
    tags: { type: Array },
  },
  created() {
    this.post = this.setPost();
  },
  data: () => ({
    post: {
      title: "",
      is_public: false,
      notification: false,
      public_at: null,
      category: "",
      series: "",
      tags: [],
    },
    dialog: false,
    categoryEndpoint: "/category/",
    seriesEndpoint: "/series/",
    tagEndpoint: "/tag/",
  }),
  methods: {
    setPost() {
      return {
        title: this.item.title,
        is_public: this.item.is_public,
        notification: this.item.notification,
        public_at: this.item.public_at,
        category: this.item.category,
        series: this.item.series,
        tags: this.item.tags,
      };
    },
    notifyMessage() {
      if (this.notification === true) {
        return "notify: send email";
      } else {
        return "silent: does not notify";
      }
    },
    publishMessage() {
      if (this.is_public === true) {
        return "public: all user will be able to read this.";
      } else {
        return "private: you can only read this.";
      }
    },
    saveDate(date) {
      this.post.public_at = date;
    },
    reflesh(endpoint) {
      this.$emit("newProps", endpoint);
    },
    editPost() {
      this.$axios
        .$put(`/post/${this.item.id}/`, this.post)
        .then((res) => {
          this.$emit("editPost");
        })
        .catch((errorMsg) => {
          console.log(errorMsg);
        })
        .finally(() => {
          this.dialog = false;
          return false;
        });
    },
    close() {
      this.dialog = false;
    },
  },
};
</script>
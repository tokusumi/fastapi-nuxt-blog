<template>
  <v-data-table
    :headers="headers"
    :items="posts"
    :server-items-length="total"
    :options.sync="options"
    :loading="loading"
    sort-by="created_by"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Posts</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn
          color="teal lighten-1"
          :loading="loading"
          dark
          class="mb-2"
          to="/post/"
          >New Item</v-btn
        >
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="showItem(item)"
        >mdi-book-open-variant</v-icon
      >
      <edit-item
        :item="item"
        :categories="categories"
        :serieses="serieses"
        :tags="tags"
        v-on:editPost="reload"
        v-on:newProps="reflesh"
      ></edit-item>
      <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>
<script>
import EditItem from "~/components/EditItem.vue";
export default {
  pageTitle: "Dashboard",
  components: {
    EditItem,
  },
  async asyncData({ app }) {
    const data = await app.$axios
      .$get("/post/")
      .then((res) => {
        return res;
      })
      .catch((e) => {
        return { data: [], max_page: 0, total: 0 };
      });
    const posts = data.data.map((x) => {
      x.category = x.category ? x.category.name || "" : "";
      x.series = x.series ? x.series.name || "" : "";
      x.tags = x.tags.map((tag) => {
        return tag.name;
      });
      return x;
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
      posts: posts,
      total: data.total,
      categoryEndpoint: "/category/",
      seriesEndpoint: "/series/",
      tagEndpoint: "/tag/",
      categories: await getValue("/category/", app.$axios),
      serieses: await getValue("/series/", app.$axios),
      tags: await getValue("/tag/", app.$axios),
    };
  },
  data: () => ({
    loading: false,
    options: {},
    headers: [
      { text: "public at", value: "public_at" },
      {
        text: "Title",
        align: "start",
        sortable: false,
        value: "title",
      },
      { text: "Author", value: "author.username" },
      { text: "Category", value: "category" },
      { text: "Series", value: "series" },
      { text: "Tags", value: "tags" },
      { text: "Is public", value: "is_public" },
      { text: "Actions", value: "actions", sortable: false },
    ],
  }),
  watch: {
    options: {
      handler() {
        this.sendGetPost();
      },
      deep: true,
    },
  },
  methods: {
    initialize() {
      this.sendGetPost();
    },
    getTags(tags) {
      return length(tags) > 0
        ? tags.map((x) => {
            return x.name;
          })
        : [];
    },
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
    showItem(item) {
      this.$router.push(`/detail/?id=${item.id}`);
    },
    editItem(item) {
      this.editedIndex = this.posts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.posts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.sendDeletePost(this.posts[index].id);
      this.initialize();
    },
    async sendGetPost() {
      const { sortBy, sortDesc, page, itemsPerPage } = this.options;
      await this.$axios
        .$get("/post/", { params: { page: page, length: itemsPerPage } })
        .then((res) => {
          this.total = res.total;
          this.posts = res.data.map((x) => {
            x.category = x.category ? x.category.name || "" : "";
            x.series = x.series ? x.series.name || "" : "";
            x.tags = x.tags.map((tag) => {
              return tag.name;
            });
            return x;
          });
        })
        .catch((e) => {});
    },
    async sendDeletePost(post_id) {
      await this.$axios
        .$delete(`/post/${post_id}/`)
        .then((res) => {})
        .catch((e) => {});
    },
    reload() {
      this.initialize();
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
  },
};
</script>
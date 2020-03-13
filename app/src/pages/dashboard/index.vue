<template>
  <v-data-table :headers="headers" :items="posts" sort-by="created_by" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Posts</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.title" label="Title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-select v-model="editedItem.category" :items="categories" label="Calories"></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-select v-model="editedItem.series" :items="serieses" label="Series"></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="8">
                    <v-select v-model="editedItem.tag" :items="tags" label="Tags" multiple chips></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-switch v-model="editedItem.is_public" :label="`${publishMessage()}`"></v-switch>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
      <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>
<script>
export default {
  async asyncData({ app }) {
    let base_url = process.client ? "http://localhost:80" : "http://fastapi:80";
    const data = await app.$axios.$get(`${base_url}/post/`);
    let categories = await app.$axios.$get(`${base_url}/category/`).catch(e => {
      return [];
    });
    const serieses = await app.$axios.$get(`${base_url}/series/`).catch(e => {
      return [];
    });
    const tags = await app.$axios.$get(`${base_url}/tag/`).catch(e => {
      return [];
    });

    return {
      posts: data,
      categories: categories.map(x => {
        return x.name;
      }),
      serieses: serieses.map(x => {
        return x.name;
      }),
      tags: tags.map(x => {
        return x.name;
      })
    };
  },
  data: () => ({
    dialog: false,
    headers: [
      { text: "Created at", value: "created_at" },
      {
        text: "Title",
        align: "start",
        sortable: false,
        value: "title"
      },
      { text: "Author", value: "author" },
      { text: "Category", value: "category" },
      { text: "Series", value: "series" },
      { text: "Tags", value: "tag" },
      { text: "Is public", value: "is_public" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    posts: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      category: "",
      series: "",
      tag: "",
      created_at: ""
    },
    defaultItem: {
      title: "",
      category: "",
      series: "",
      tag: "",
      created_at: ""
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.sendGetPost();
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

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.posts[this.editedIndex], this.editedItem);
      } else {
        this.posts.push(this.editedItem);
      }
      this.close();
    },
    publishMessage() {
      if (this.editedItem.is_public === true) {
        return "public";
      } else {
        return "private";
      }
    },
    async sendGetPost() {
      await this.$axios
        .$get("http://0.0.0.0:80/post/")
        .then(res => {
          this.posts = res;
        })
        .catch(e => {});
    },
    async sendDeletePost(post_id) {
      console.log(post_id);
      await this.$axios
        .$delete(`http://0.0.0.0:80/post/${post_id}/`)
        .then(res => {})
        .catch(e => {});
    }
  }
};
</script>
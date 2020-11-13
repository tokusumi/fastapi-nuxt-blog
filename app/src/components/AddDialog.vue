<template>
  <v-dialog v-model="dialog" width="500">
    <template v-slot:activator="{ on }">
      <v-btn icon>
        <v-icon v-on="on">mdi-pencil-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">add {{ field }}</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-text-field v-model="value" :label="field"></v-text-field>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="add">Add</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
 
 <script>
export default {
  name: "AddDialog",
  props: {
    endpoint: "",
    field: "",
  },
  data: () => ({
    dialog: false,
    value: "",
  }),
  methods: {
    add() {
      this.$axios
        .$post(this.endpoint, {
          name: this.value,
        })
        .then((res) => {
          this.$emit("new", this.endpoint);
        })
        .catch((errorMsg) => {
          console.log(errorMsg);
        })
        .finally(() => {
          this.dialog = false;
          return false;
        });
    },
  },
};
</script>
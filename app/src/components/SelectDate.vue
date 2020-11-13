<template>
  <v-menu
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    :return-value.sync="_date"
    transition="scale-transition"
    offset-y
    min-width="290px"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        v-model="_date"
        label="Public at"
        prepend-icon="mdi-calendar"
        clearable
        readonly
        @click:clear="clear"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker v-model="_date" no-title scrollable>
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
      <v-btn text color="primary" @click="save">OK</v-btn>
    </v-date-picker>
  </v-menu>
</template>
<script>
export default {
  name: "SelectDate",
  props: {
    date: {
      validator: (prop) => typeof prop === "string",
    },
  },
  created() {
    this._date = this.setDate();
  },
  data: () => ({
    menu: false,
    _date: null,
  }),
  methods: {
    setDate() {
      return this.date.slice(0, 10);
    },
    clear() {
      this._date = this.setDate();
      this.$emit("save", this._data + "T00:00:00");
    },
    save() {
      this.$refs.menu.save(this._date);
      this.$emit("save", this._date + "T00:00:00");
    },
  },
};
</script>
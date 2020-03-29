<template>
  <v-container fluid>
    <v-layout column>
      <v-card>
        <v-card-text>
          <v-flex class="mb-4">
            <v-avatar size="96" class="mr-4">
              <img v-if="form.imgUrl" :src="form.imgUrl" alt="Avatar" />
              <v-icon v-else size="96">mdi-account</v-icon>
            </v-avatar>
            <v-btn class="teal lighten-1" @click.native="toUpdate">Change profile</v-btn>
          </v-flex>
          <v-text-field v-model="form.userName" label="Username" readonly></v-text-field>
          <v-text-field v-model="form.contactEmail" label="Email Address" readonly></v-text-field>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  pageTitle: "Profile",
  data() {
    return {
      form: {
        imgUrl: this.$auth.user.icon,
        userName: this.$auth.user.username,
        contactEmail: this.$auth.user.email
      }
    };
  },
  methods: {
    toUpdate() {
      this.$router.push("/profile/update/");
    }
  }
};
</script>
<template>
  <v-app>
    <v-container fluid>
      <v-card class="mx-auto" max-width="400px">
        <v-card-title>
          <v-row>
            <v-col class="d-flex" cols="12" xs="12" sm="6">
              <v-row align="center" justify="center">
                <v-avatar size="96" class="mr-4">
                  <img v-if="form.imgUrl" :src="form.imgUrl" alt="Avatar" />
                  <v-icon v-else size="96">mdi-account</v-icon>
                </v-avatar>
              </v-row>
            </v-col>
            <v-col class="d-flex" cols="12" xs="12" sm="6">
              <v-row align="center" justify="left">
                <v-btn class="teal lighten-1" @click.native="toUpdate"
                  >Change profile</v-btn
                >
              </v-row>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="form.userName"
            label="Username"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="form.contactEmail"
            label="Email Address"
            readonly
          ></v-text-field>
        </v-card-text>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
export default {
  pageTitle: "Profile",
  data() {
    return {
      form: {
        imgUrl: this.$auth.user.icon,
        userName: this.$auth.user.username,
        contactEmail: this.$auth.user.email,
      },
    };
  },
  methods: {
    toUpdate() {
      this.$router.push("/profile/update/");
    },
  },
};
</script>
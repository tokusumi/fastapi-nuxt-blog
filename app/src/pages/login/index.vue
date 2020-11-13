<template>
  <v-app>
    <v-container fluid>
      <v-card class="mx-auto" max-width="400px">
        <v-card-title>Login Form</v-card-title>

        <v-form>
          <v-container>
            <v-text-field
              v-model="login.username"
              label="E-mail"
              ref="username"
            ></v-text-field>
            <v-text-field
              v-model="login.password"
              :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
              :type="show ? 'text' : 'password'"
              name="password"
              label="Password"
              hint="At least 8 characters"
              class="input-group--focused"
              @click:append="show = !show"
            ></v-text-field>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="mr-4" @click="userLogin">Login</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
export default {
  middleware({ store, redirect }) {
    if (store.$auth.loggedIn) {
      redirect("/");
    }
  },
  data() {
    return {
      show: false,
      login: {
        username: "",
        password: "",
      },
    };
  },
  mounted() {
    this.$refs.username.focus();
  },
  methods: {
    userLogin() {
      let formData = new FormData();
      formData.append("username", this.login.username);
      formData.append("password", this.login.password);
      try {
        this.$auth
          .loginWith("local", { data: formData })
          .then((res) => {
            console.log("success");
          })
          .catch((err) => {
            console.log(err);
          });
      } catch (err) {
        (err) => {
          console.log(err);
        };
      }
    },
  },
};
</script>
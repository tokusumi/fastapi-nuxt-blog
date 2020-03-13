<template>
  <v-container>
    <v-card class="mx-auto" max-width="600">
      <v-card-title>Login Form</v-card-title>

      <v-form>
        <v-container>
          <v-text-field v-model="login.email" label="E-mail"></v-text-field>
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
          <v-btn to="/register">Register</v-btn>
          <v-btn class="mr-4" @click="userLogin">Login</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      login: {
        email: "",
        password: ""
      }
    };
  },
  methods: {
    async userLogin() {
      try {
        let response = await this.$auth.loginWith("local", {
          data: this.login
        });
        console.log(response);
      } catch (err) {
        console.log(err);
      }
    }
  }
};
</script>
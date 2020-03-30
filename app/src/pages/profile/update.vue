<template>
  <v-container fluid>
    <v-layout column>
      <v-card>
        <v-card-text>
          <v-flex class="mb-4">
            <v-avatar size="96" class="mr-4">
              <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" />
              <v-icon v-else size="96">mdi-account</v-icon>
            </v-avatar>
            <file-upload
              class="mr-4"
              :endpoint="endpoint"
              v-on:fileUploadEvent="changeAvatar"
              v-on:fileSelectEvent="selectAvatar"
            />
          </v-flex>
          <v-text-field v-model="form.userName" label="Username"></v-text-field>
          <v-text-field v-model="form.contactEmail" label="Email Address"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn @click.native="toView">Reset</v-btn>
          <v-btn color="teal lighten-1" :loading="loading" @click.native="submit">
            <v-icon left dark>mdi-check</v-icon>Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import FileUpload from "~/components/FileUpload.vue";
export default {
  pageTitle: "Profile",
  components: {
    FileUpload
  },
  data() {
    return {
      loading: false,
      form: {
        imgUrl: this.$auth.user.icon,
        userName: this.$auth.user.username,
        contactEmail: this.$auth.user.email
      },
      avatarUrl: this.$auth.user.icon,
      endpoint: "/users/image/"
    };
  },
  methods: {
    async submit() {
      this.loading = true;
      await this.$axios
        .$put(`/users/`, {
          icon: this.form.imgUrl,
          username: this.form.userName,
          email: this.form.contactEmail
        })
        .then(res => {
          this.$router.push("/profile/");
        })
        .catch(e => {
          console.log(e);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    clear(user) {
      this.form = {
        imgUrl: user.icon,
        userName: user.username,
        contactEmail: user.email
      };
    },
    selectAvatar(resCode, target) {
      let reader = new FileReader();
      reader.onload = e => {
        this.avatarUrl = e.target.result;
      };
      reader.readAsDataURL(target.files[0]);
    },
    changeAvatar(resCode, data) {
      this.avatarUrl = data.icon;
      this.form.imgUrl = data.icon;
    },
    toView() {
      this.$router.push("/profile/");
    }
  }
};
</script>
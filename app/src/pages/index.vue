<template>
  <v-app>
    <v-container fluid fill-height>
      <v-row align="center" justify="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-row align="center" justify="center">
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">
                <nuxt-link to="/post/">
                  <write-logo />
                </nuxt-link>
              </v-row>
            </v-col>
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">WRITE</v-row>
            </v-col>
          </v-row>
        </v-col>
        <v-col class="d-flex" cols="12" sm="6">
          <v-row align="center" justify="center">
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">
                <nuxt-link to="/dashboard/">
                  <book-logo />
                </nuxt-link>
              </v-row>
            </v-col>
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">EDIT</v-row>
            </v-col>
          </v-row>
        </v-col>
        <v-col class="d-flex" cols="12" sm="6">
          <v-row align="center" justify="center">
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">
                <nuxt-link to="/list/">
                  <rocket-logo />
                </nuxt-link>
              </v-row>
            </v-col>
            <v-col class="d-flex" cols="12">
              <v-row align="center" justify="center">VIEW</v-row>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import WriteLogo from "~/components/WriteLogo.vue";
import RocketLogo from "~/components/RocketLogo.vue";
import BookLogo from "~/components/BookLogo.vue";

export default {
  components: {
    WriteLogo,
    RocketLogo,
    BookLogo,
  },
  data() {
    return {
      show: false,
    };
  },
};
</script>

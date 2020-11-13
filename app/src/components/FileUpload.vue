<template>
  <v-container grid-list-md text-xs-center fill-height>
    <v-layout row wrap align-center>
      <input
        ref="image"
        class="hide-input"
        type="file"
        accept="image/*"
        @change="imageSelected"
      />
      <v-btn v-if="isNotUploaded" class="select-button" @click="selectImage">
        Select
        <v-icon right>mdi-cloud-upload</v-icon>
      </v-btn>
      <v-btn
        v-else
        class="upload-button"
        color="teal lighten-1"
        @click="uploadImage"
      >
        Upload
        <v-progress-circular
          v-if="loading"
          size="24"
          :indeterminate="loading"
        ></v-progress-circular>
        <v-icon v-else right color="white">mdi-cloud-upload</v-icon>
      </v-btn>
    </v-layout>
  </v-container>
</template>
 <script>
export default {
  name: "FileUpload",
  props: {
    endpoint: "",
  },
  data: () => ({
    isNotUploaded: true,
    photo: "",
    photoName: "",
    loading: false,
  }),
  methods: {
    selectImage() {
      this.photo = this.$refs.image.click();
    },
    imageSelected(e) {
      this.$emit("input", e.target.files[0]);
      this.photo = this.$refs.image.files[0];
      this.photoName = this.photo.name;
      this.isNotUploaded = false;
      this.$emit("fileSelectEvent", 0, e.target);
    },
    async uploadImage() {
      let formData = new FormData();
      formData.append("file", this.photo);
      this.$axios
        .$post(this.endpoint, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          this.$emit("fileUploadEvent", 0, res);
        })
        .catch((errorMsg) => {
          this.$emit("fileUploadEvent", -1, "");
        })
        .finally(() => {
          this.isNotUploaded = true;
          return false;
        });
    },
    clear() {
      this.isNotUploaded = true;
      this.photo = "";
      this.photoName = "";
    },
  },
};
</script>
 
 <style scoped>
.hide-input {
  display: none;
}
* {
  text-transform: none !important;
}
.select-button {
  border-radius: 50px;
  color: black;
}
.upload-button {
  border-radius: 50px;
  color: white;
}
</style>

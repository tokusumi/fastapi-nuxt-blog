<template>
  <div class="box-book" />
</template>


<style scoped>
.box-book {
  width: 200px;
  height: 200px;
  box-sizing: border-box;
  background: url(https://dev-blog-s3.s3-ap-northeast-1.amazonaws.com/static/home/books.svg)
    no-repeat center;
  background-size: 100% auto;
}

.VuetifyLogo {
  width: 180px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}
</style>

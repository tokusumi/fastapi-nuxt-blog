<template>
  <div class="box-write" />
</template>


<style scoped>
.box-write {
  width: 200px;
  height: 200px;
  box-sizing: border-box;
  background: url(https://dev-blog-s3.s3-ap-northeast-1.amazonaws.com/static/home/design.svg)
    no-repeat center;
  background-size: 100% auto;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}
</style>

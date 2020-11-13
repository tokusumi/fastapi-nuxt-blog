<template>
  <v-app white>
    <v-card color="grey lighten-4" flat height="50px" tile>
      <v-navigation-drawer v-model="leftDrawer" :left="left" temporary fixed>
        <v-list>
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            :to="item.to"
            router
            exact
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar dense fixed>
        <v-app-bar-nav-icon
          @click.stop="leftDrawer = !leftDrawer"
        ></v-app-bar-nav-icon>

        <v-toolbar-title>{{ title }}</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon to="/post/">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>

        <v-btn icon to="/dashboard">
          <v-icon>mdi-dresser</v-icon>
        </v-btn>

        <v-btn icon to="/profile">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </v-app-bar>
    </v-card>

    <v-content>
      <v-container>
        <nuxt keep-alive />
      </v-container>
    </v-content>

    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      clipped: false,
      fixed: false,
      title: "Blog",
      left: true,
      leftDrawer: false,
      items: [
        {
          icon: "mdi-apps",
          title: "Home",
          to: "/",
        },
        {
          icon: "mdi-newspaper-variant",
          title: "List",
          to: "/list",
        },
        {
          icon: "mdi-pencil",
          title: "Post",
          to: "/post",
        },
        {
          icon: "mdi-dresser",
          title: "dashboard",
          to: "/dashboard",
        },
      ],
    };
  },
};
</script>
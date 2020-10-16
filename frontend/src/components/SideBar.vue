<template>
  <!-- Sidebar -->
    <ul :class="['navbar-nav', 'bg-gradient-primary', 'sidebar', 
       'sidebar-dark', 'accordion', isToggled?'toggled':'']" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon">
          <b-icon icon="x-diamond"></b-icon>
        </div>
        <div class="sidebar-brand-text mx-3">YUFU 量化</div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item active">
        <a class="nav-link" href="index.html">
          <b-icon icon="cpu" class="mr-2"></b-icon>
          <span>机器人</span>
        </a>
      </li>

      <!-- Divider -->
      <!-- <hr class="sidebar-divider"> -->

      <!-- Heading -->
      <!-- <div class="sidebar-heading">
        策略
      </div> -->

      <!-- Nav Item - Pages Collapse Menu -->
      <li class="nav-item">
        <a class="nav-link" href="#" >
          <b-icon icon="graph-up" class="mr-2"></b-icon>
          <span>策略</span>
        </a>
      </li>

   

      <!-- Divider -->
      <!-- <hr class="sidebar-divider"> -->

      <!-- Heading -->
      <!-- <div class="sidebar-heading">
        接入
      </div> -->

      <!-- Nav Item - Charts -->
      <li class="nav-item">
        <a class="nav-link" href="charts.html">
          <b-icon icon="key" class="mr-2"></b-icon>
          <span>接入</span></a>
      </li>

      <!-- Divider -->
      <!-- <hr class="sidebar-divider d-none d-md-block"> -->

      <!-- Sidebar Toggler (Sidebar) -->
      <div class="text-center d-none d-md-inline">
        <!-- <button class="rounded-circle border-0" id="sidebarToggle" @click="sidebarToggle"></button> -->
        <b-button class="rounded-circle border-0 mt-3" id="sidebarToggle" @click="sidebarToggle" >
          <b-icon :icon="isToggled? 'chevron-right':'chevron-left'" class="toggle-icon" ></b-icon>
        </b-button>
      </div>

    </ul>
    <!-- End of Sidebar -->
</template>

<script>
export default {
  data() {
    return {
      isToggled: false,
    }
  },
  methods: {
    sidebarToggle() {
      this.isToggled = !this.isToggled;
    }
  }
}
</script>

<style lang="scss">
@import '../assets/base.scss';
@import '../assets/sidebar.scss';

// .sidebar {
//     background: red;
// }
</style>
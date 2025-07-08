import { createRouter, createWebHistory } from "vue-router";
import SearchInterface from "./components/SearchInterface.vue";
import CompanyDetail from "./components/CompanyDetail.vue";
import EmployeeDetail from "./components/EmployeeDetail.vue";

const routes = [
  {
    path: "/",
    component: SearchInterface,
  },
  {
    path: "/companies/:id",
    component: CompanyDetail,
    props: true,
  },
  {
    path: "/employees/:id",
    component: EmployeeDetail,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

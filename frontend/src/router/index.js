import VueRouter from "vue-router";
import RobotCreateView from "../views/RobotCreateView";
import RobotListView from "../views/RobotListView";
import RobotView from "../views/RobotView";
import LoginView from "../views/LoginView";
import ConnectView from "../views/ConnectView";
import Account from "../views/Account";
import StrategyTemplateListView from "../views/StrategyTemplateListView";
import Vue from 'vue'

Vue.use(VueRouter)
const routes = [
    {path: '/', component: RobotListView},
    {path: '/robot/list', component: RobotListView},
    {path: '/robot/create', component: RobotCreateView},
    // {path: '/robot/update', component: RobotCreateView},
    {path: '/robot/:id', component: RobotView},
    {path: '/login', component: LoginView},
    {path: '/connect', component: ConnectView},
    {path: '/account', component: Account},
    {path: '/strategy-template/list', component: StrategyTemplateListView},
]
const router = new VueRouter({
    routes // (缩写) 相当于 routes: routes
})

export default router
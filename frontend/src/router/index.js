import VueRouter from "vue-router";
import RobotCreateView from "../views/RobotCreateView";
import RobotListView from "../views/RobotListView";
import RobotUpdateView from "../views/RobotUpdateView";
import RobotView from "../views/RobotView";
import LoginView from "../views/LoginView";
import CredentialView from "../views/CredentialView";
import Account from "../views/Account";
import StrategyListView from "../views/StrategyListView";
import StrategyCreateView from "../views/StrategyAddView";
import StrategyDetailView from "../views/StrategyDetailView";
import Vue from 'vue'

Vue.use(VueRouter)
const routes = [
    {path: '/', component: RobotListView},
    {path: '/robot/list', name: 'robot-list', component: RobotListView},
    {path: '/robot/create', name: 'robot-create', component: RobotCreateView},
    {path: '/robot/:id', name: 'robot', component: RobotView},
    {path: '/robot/:id/update', name: 'robot-update', component: RobotUpdateView},
    {path: '/login', component: LoginView},
    {path: '/credential', name: 'credential', component: CredentialView},
    {path: '/account', component: Account},
    {path: '/strategy/list', name: 'strategy-list', component: StrategyListView},
    {path: '/strategy/add', name: 'strategy-add', component: StrategyCreateView},
    {path: '/strategy/:id', name: 'strategy-detail', component: StrategyDetailView},
]
const router = new VueRouter({
    routes // (缩写) 相当于 routes: routes
})

export default router
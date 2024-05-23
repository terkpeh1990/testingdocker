from django.urls import path
from . import team,level,agent,ticket

app_name = 'helpdesk'

urlpatterns = [
    # team start
    path('team/',team.team, name='team-list'),
    path('team/new/',team.add_team, name='new-team'),
    path('team/<str:team_id>/update/',team.edit_team, name='edit-team'),
    path('team/<str:team_id>/delete/',team.delete_team, name='delete-team'),
    path('team/upload/',team.team_upload,name='upload-team'),
    # team end

    #level Start
    path('level/',level.level,name='level-list'),
    path('level/new/',level.add_level, name='new-level'),
    path('level<str:level_id>/update/',level.edit_level, name='edit-level'),
    path('level/<str:level_id>/delete/',level.delete_level, name='delete-level'),
    path('level/upload/',level.level_upload,name='upload-level'),
    #level end

    # Agent Start
    path('agent/load_subcategory/',agent.load_subcategory,name="load-subcategory"),
    path('agent/load_user/',agent.load_user,name="load_user"),
    path('agent/',agent.agent,name='agent-list'),
    path('agent/new/',agent.add_agent, name='new-agent'),
    path('agent/<str:agent_id>/update/',agent.edit_agent, name='edit-agent'),
    path('agent/<str:agent_id>/delete/',agent.delete_agent, name='delete-agent'),
    path('agent/upload/',agent.agent_upload,name='upload-agent'),

    # Agent End
    
    # Ticket Start
    path('ticket/allticket/',ticket.allticket,name='ticket-list'),
    path('ticket/agentticket/',ticket.agentticket,name='agent-ticket-list'),
    path('ticket/new/',ticket.add_ticket,name='new-ticket'),
    path('ticket/<str:ticket_id>/update/',ticket.edit_ticket,name='edit-ticket'),
    path('ticket/<str:ticket_id>/detail/',ticket.ticketdetail,name='ticket-detail'),
    path('ticket/<str:ticket_id>/agentdetail/',ticket.agentticketdetail,name='agent-ticket-detail'),
    path('ticket/loadagent/',ticket.load_agent,name='load-agent'),
    path('ticket/<str:ticket_id>/assign/',ticket.assigned_ticket,name='assign-agent'),
    path('ticket/<str:ticket_id>/excalate/',ticket.excalate_ticket,name='excalate-ticket'),
    path('ticket/<str:ticket_id>/comment/',ticket.comment_ticket,name='comment-ticket'),
    path('ticket/<str:ticket_id>/close/',ticket.closeticket,name='close-ticket'),
    path('ticket/<str:ticket_id>/delete/',ticket.delete_ticket,name='delete-ticket'),
    path('ticket/ontime_ticket/',ticket.ontime_ticket,name='ontime-ticket'),
    path('ticket/notontime_ticket/',ticket.notontime_ticket,name='notontime-ticket'),
    path('ticket/open_ticket/',ticket.open_ticket,name='open-ticket'),
    path('ticket/dashboard/',ticket.ticketdashboard,name='ticketdashboard'),
    # Ticket End

]
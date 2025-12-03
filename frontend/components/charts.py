import streamlit as st
import plotly.graph_objects as go

def plot_macros(protein, carbs, fat):
    """
    Creates a donut chart for macronutrients.
    """
    labels = ['Protein', 'Carbs', 'Fat']
    values = [protein, carbs, fat]
    colors = ['#00CC96', '#EF553B', '#FFA15A'] # Green, Red, Orange

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.4,
        marker=dict(colors=colors)
    )])
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), 
        height=200,
        showlegend=True
    )
    
    return fig

def plot_calories_gauge(current, target):
    """
    Creates a gauge chart showing progress towards daily limit.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Calories (Meal)"},
        delta = {'reference': target, 'increasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, target], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1f77b4"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, target*0.5], 'color': '#e6f2ff'},
                {'range': [target*0.5, target*0.8], 'color': '#99ccff'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target}}))
    
    fig.update_layout(height=250, margin=dict(t=30, b=0, l=20, r=20))
    return fig
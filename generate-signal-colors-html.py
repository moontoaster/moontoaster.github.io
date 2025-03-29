#!/usr/bin/env python3

import json

def join_strs(sl):
    return ''.join(sl)

def single_color(color, identifier=None):
    maybe_identifier = f'<span class="color-id">{identifier}</span>' if identifier else ''

    return f'''
    <div class="color">
        <div class="color-circle" style="background: {color}"></div>
        {maybe_identifier}
        <span class="color-hex">{color}</span>
    </div>
    '''

def gradient(degrees, colors, positions, identifier=None):
    maybe_identifier = f'<span class="color-id">{identifier}</span>' if identifier else ''
    colors_list = join_strs(map(lambda c: f'<span class="color-hex">{c}</span>', colors))

    gradient_components = ', '.join(map(lambda c: f'{c[0]} {c[1] * 100}%', zip(colors, positions)))

    return f'''
    <div class="color">
        <div class="color-circle" style="background: linear-gradient({degrees}deg, {gradient_components})"></div>
        {maybe_identifier}
        {colors_list}
    </div>
    '''

with open('signal-colors.json', 'rb') as colors_json:
    colors = json.load(colors_json)

with open('signal-colors.html', 'w') as colors_html:
    name_colors_light = join_strs(map(lambda c: single_color(c['light']), colors['nameColors']))
    name_colors_dark = join_strs(map(lambda c: single_color(c['dark']), colors['nameColors']))
    bubble_colors_solid = join_strs(map(lambda c: single_color(c['color'], identifier=c['id']), colors['bubbleSolidColors']))
    bubble_colors_gradient = join_strs(map(lambda c: gradient(c['degrees'], c['colors'], c['positions'], c['id']), colors['bubbleGradientColors']))

    html = f'''
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href="signal-colors.css">
        </head>

        <body>
            <h1>Name colors (light)</h1>
            <div class="color-grid">
                {name_colors_light} 
            </div>
            
            <h1>Name colors (dark)</h1>
            <div class="color-grid">
                {name_colors_dark} 
            </div>

            <h1>Bubble colors (solid)</h1>
            <div class="color-grid">
                {bubble_colors_solid}
            </div>
            
            <h1>Bubble colors (gradient)</h1>
            <div class="color-grid">
                {bubble_colors_gradient}
            </div>

            <hr>
            Sourced from 
            <a href="https://github.com/signalapp/Signal-Android/blob/main/app/src/main/java/org/thoughtcrime/securesms/conversation/colors/ChatColorsPalette.kt">
                https://github.com/signalapp/Signal-Android/blob/main/app/src/main/java/org/thoughtcrime/securesms/conversation/colors/ChatColorsPalette.kt
            </a>
        </body>
    </html>
    '''

    colors_html.write(html)

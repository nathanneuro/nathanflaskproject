#utils.py
import pandas as pd
import pygal


def norm_df (df, weights, targets):
    df['norm_income'] = df['income']*weights[0]
    df['norm_gdp_obs'] = df['gdp_obs']*weights[1]
    df['norm_gdp_proj'] = df['gdp_proj']*weights[2]
    df['norm_digi_read'] = df['digi_read']*weights[3]
    df['norm_digi_math'] = df['digi_math']*weights[4]
    df['norm_pisa_math'] = df['pisa_math']*weights[5]
    df['norm_pisa_read'] = df['pisa_read']*weights[6]
    df['norm_pisa_sci'] = df['pisa_sci']*weights[7]
    df['norm_top_mathers'] = df['top_mathers']*weights[8]
    if len(weights) == 10:
        df['norm_citi_score'] = df['citi_score']*weights[9]
        df['weight_score'] = (df['income']*weights[0] + df['gdp_obs']*weights[1] + df['gdp_proj']*weights[2] + df['digi_read']*weights[3] + df['digi_math']*weights[4] + df['pisa_math']*weights[5] + df['pisa_read']*weights[6] + df['pisa_sci']*weights[7] + df['top_mathers']*weights[8] + df['citi_score']*weights[9])/10
    else:
        df['weight_score'] = (df['income']*weights[0] + df['gdp_obs']*weights[1] + df['gdp_proj']*weights[2] + df['digi_read']*weights[3] + df['digi_math']*weights[4] + df['pisa_math']*weights[5] + df['pisa_read']*weights[6] + df['pisa_sci']*weights[7] + df['top_mathers']*weights[8])/9

    #Fancy version (but not yet functional) for refactoring someday
    #df['weight_score'] = 0
    #for w in weights:
    #    df["norm_{0}".format(targets[w])] = df["{0}".format(targets[w])]*weights[w]
    #    df['weight_score'] = df['weight_score']+df["norm_{0}".format(targets[w])]
    
        
    return df


def line_plot(df, subjects, factors, give_title):
    plot = pygal.Line(x_label_rotation=20, stroke_style={'width': 3}, margin=10, y_title='Factor as % of Mean * Weight')
    plot.x_labels = factors

    for subject in range(subjects):
        row_values = df.iloc[subject,]
        row_values = row_values.values
        print(row_values[1:])
        cols = df.columns.tolist()
        print(cols[1:])
        plot.add(df.index[subject], row_values[1:])

    return plot.render()

def world_plot(df, give_title):
    plot = pygal.maps.world.World()
    #worldmap_chart.title = give_title
    codes = df['pygal_code'].tolist()
    scores = df['weight_score'].tolist()
    world_dict = dict(zip(codes, scores))
    plot.add('Weighted Score', world_dict)
    return plot.render(is_unicode=True)


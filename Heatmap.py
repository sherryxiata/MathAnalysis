# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 15:26
# @Author  : wenlei

'''
调用百度地图api绘制各个省份获奖人数（参与人数）的热力图
'''

from config import *

# 按地图省份绘制每个省份的获奖人数热力图
# 调用百度地图API获取每个学校的经纬度信息
def get_school_info():
    df = pd.read_csv(save_path+'各学校获奖人数统计.csv',encoding='utf_8_sig')
    lng_set = [] #经度
    lat_set=[] #纬度
    for school in df['学校名称']:
        print(school)
        try:
            location = geolocator.geocode(school, timeout=300)
            lng_lat=location.raw['location']
            lng,lat=lng_lat['lng'],lng_lat['lat']
            print(lng,lat)
            lng_set.append(lng)
            lat_set.append(lat)
        except Exception as e:
            print(e)
            time.sleep(5)
            lng_set.append(np.nan)
            lat_set.append(np.nan)

    df['lng']=lng_set
    df['lat']=lat_set
    df=df[['学校名称','获奖总人数','lng','lat']]
    df.to_csv(save_path+'school_loc_prize_nums.csv',encoding='utf_8_sig', index=False,float_format='%.6f')
    print(df.head())

# 绘制热力地图
def draw_heatmap(input_path,out_path):
    df=pd.read_csv(input_path,encoding='utf_8_sig')
    df=df[df['lng']>0]
    rows=df.shape[0]
    fout=open(out_path,'w',encoding="utf-8")
    fout.write(
'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
    <title>2018研究生建模成绩地理位置分析</title>
    <link rel="stylesheet" href="http://cache.amap.com/lbs/static/main1119.css"/>
    <script src="http://webapi.amap.com/maps?v=1.3&key=your-personal-key"></script>
    <script type="text/javascript" src="http://cache.amap.com/lbs/static/addToolbar.js"></script>
    <script type="text/javascript" src="http://a.amap.com/jsapi_demos/static/resource/heatmapData.js"></script>
</head>
<body>
    <div id="container">
    </div>
    <div class="button-group">
        <input type="button" class="button" value="显示热力图" onclick="heatmap.show()"/>
        <input type="button" class="button" value="关闭热力图" onclick="heatmap.hide()"/>
    </div>
    <script>
        var map = new AMap.Map("container", {
            resizeEnable:false,
            center: [121.5197936,31.2874348],
            zoom: 7
        });
        if (!isSupportCanvas()) {
            alert('热力图仅对支持canvas的浏览器适用,您所使用的浏览器不能使用热力图功能,请换个浏览器试试~')
        }'''
    )
    fout.write("\n\t\t var points = [\n")
    for i in range(0,rows-1):
        fout.write("\t\t\t{'lat':%f,'lng':%f,'count':%d},\n"%(df.iat[i,3],df.iat[i,2],df.iat[i,1]))
    fout.write("\t\t\t{'lat':%f,'lng':%f,'count':%d}];"%(df.iat[-1,3],df.iat[-1,2],df.iat[-1,1]))
    fout.write(
    '''
        //详细的参数,可以查看heatmap.js的文档 http://www.patrick-wied.at/static/heatmapjs/docs.html
        //参数说明如下:
        /* visible 热力图是否显示,默认为true
         * opacity 热力图的透明度,分别对应heatmap.js的minOpacity和maxOpacity
         * radius 势力图的每个点的半径大小   
         * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
         *	{
         .2:'rgb(0, 255, 255)',
         .5:'rgb(0, 110, 255)',
         .8:'rgb(100, 0, 255)'
         }
         其中 key 表示插值的位置, 0-1 
         value 为颜色值 
         */
        var heatmap;
        map.plugin(["AMap.Heatmap"], function() {
            //初始化heatmap对象
            heatmap = new AMap.Heatmap(map, {
                radius: 15, //给定半径
                opacity: [0, 0.8]
                /*,gradient:{
                 0.5: 'blue',
                 0.65: 'rgb(117,211,248)',
                 0.7: 'rgb(0, 255, 0)',
                 0.9: '#ffea00',
                 1.0: 'red'
                 }*/
            });
            //设置数据集
            heatmap.setDataSet({
                data: points,
                max: 5
            });
        });
        //判断浏览区是否支持canvas
        function isSupportCanvas() {
            var elem = document.createElement('canvas');
            return !!(elem.getContext && elem.getContext('2d'));
        }
    </script>
</body>
</html>
'''
    )
    fout.close()

